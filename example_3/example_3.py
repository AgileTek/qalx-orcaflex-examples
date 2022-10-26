import itertools
import os
import sys
from os import PathLike
from pathlib import Path
from tempfile import mkdtemp

import OrcFxAPI as ofx
import qalx_orcaflex.data_models as dm
from qalx_orcaflex.core import ModelSource, OrcaFlexBatch, QalxOrcaFlex

# Define direction and offset parameters
DIRECTIONS = zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(0, 316, 45))
X_POSITIONS = [("NEAR", -40), ("FAR", -140)]


def build_and_run_batch(batch_name: str, base_path: PathLike):
    # Instantiate `qalx` session
    qfx = QalxOrcaFlex()

    # Configure batch
    ofx_batch = OrcaFlexBatch(
        name=batch_name,
        session=qfx,
        batch_options=dm.BatchOptions(
            # The queue names match those in `ofx_factory.plan`
            batch_queue="example-batch-queue",
            sim_queue="example-sim-queue",
        ),
        verbose=True,
        meta={"cable_size": "3x500"},
    )

    # Specify result metrics to extract from simulation
    results = [
        # Assumes the objects are present in the .dat files
        dm.RangeGraph(object="Riser with Flexjoint", variable="Effective Tension"),
        dm.RangeGraph(object="Riser with Flexjoint", variable="Curvature"),
    ]

    # Define model views to generate from simulation
    model_views = [
        dm.ModelView.wire_frame_from_form_str(
            "SIDE", "Global	1340.0	520.0	37.0	-450.0	270	0	0	1600	900"
        ),
        dm.ModelView.wire_frame_from_form_str(
            "TOP", "Global	1340.0	520.0	37.0	-450.0	270	90	0	1600	900"
        ),
    ]

    # Handle if the provided base model path is a relative path
    if not os.path.isabs(base_path):
        # Form the abspath from the provided relpath
        base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), base_path)

    # Instantiate base model
    m = ofx.Model(base_path)

    # Use context manager to dynamically build load cases
    with ofx_batch as batch:
        # Iterate through all combination of `DIRECTIONS` and `X_POSITIONS`
        for (direction, d), (offset, x) in itertools.product(DIRECTIONS, X_POSITIONS):
            m.environment.RefCurrentDirection = d
            m.environment.WaveDirection = d
            m["FPSO"].InitialX = x

            # Create a `ModelSource` object
            source = ModelSource(m, name=f"{direction}__{offset}")

            # Define the load case information
            lci = dm.LoadCaseInfo(
                raw_info=[
                    dm.RawInfo(key="offset", value=offset),
                    dm.RawInfo(key="direction", value=direction),
                ],
                model_info=[
                    dm.ModelInfo(
                        object_name="Environment",
                        data_name="WaveDirection",
                        alias="EnvDir",
                    )
                ],
            )

            # Add load case to batch
            batch.add(
                source=source,
                required_results=results,
                model_views=model_views,
                load_case_info=lci,
            )

    # Context manager waits for batch sims to complete and extract results
    with ofx_batch.when_complete():
        print(f"{batch_name} is complete.")

        # Create temporary directory in which model view images will be saved
        temp_dir = Path(mkdtemp("OFX_MODEL_VIEWS"))

        # Iterates through each load case of the completed batch
        for case_name, case in ofx_batch.group_batch.sets.items():

            # Uses the load case qalx set GUID to get the saved views
            load_case = qfx.set.get(case.guid, fields=["items.saved_views"])
            views = load_case["items"]["saved_views"]

            # Iterates through the saved views
            for _, view_guid in views.data.items():
                # Get the actual image file from the qalx item GUID
                view_file = qfx.item.get(view_guid)

                # Name and save the file to the local temp directory
                save_name = f"{case_name}-{view_file['file']['name']}"
                view_file.save_file_to_disk(temp_dir, filename=save_name)

        # Open the temp directory
        os.startfile(temp_dir)


if __name__ == "__main__":
    # Main functionality takes command line arguments and runs script
    _, batch_name, base_model = sys.argv
    build_and_run_batch(batch_name, base_model)
