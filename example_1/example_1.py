import os.path
import sys
from os import PathLike
from pprint import pprint

import qalx_orcaflex.data_models as dm
from qalx_orcaflex.core import DirectorySource, OrcaFlexBatch, QalxOrcaFlex


def build_and_run_batch(batch_name, directory_path: PathLike):
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
    )

    # Specify result metrics to extract from simulation
    results = [
        # Assumes the objects are present in the .dat files
        dm.RangeGraph(
            object="Riser with Flexjoint",
            variable="Effective Tension",
        ),
        dm.RangeGraph(object="Riser with Flexjoint", variable="Curvature"),
    ]

    # Use context manager to specify .dat files and results
    with ofx_batch as batch:
        if not os.path.isabs(directory_path):
            # Form the abspath from the provided relpath
            directory_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), directory_path
            )

        # Create a `DirectorySource` object that the batch can iterate through
        source = DirectorySource(directory_path)
        batch.add(source=source, required_results=results)

    # Context manager waits for batch sims to complete and extract results
    with ofx_batch.when_complete():
        print(f"{batch_name} is complete.")

        # Get results summary and print to console
        results_summary = qfx.get_batch_results_summary(batch_name)
        for result in results_summary["Range Graphs"]:
            print(f"{result}:\n\n")
            pprint(results_summary["Range Graphs"][result])


if __name__ == "__main__":
    # Main functionality takes command line arguments and runs script
    _, batch_name, directory = sys.argv
    build_and_run_batch(batch_name, directory)
