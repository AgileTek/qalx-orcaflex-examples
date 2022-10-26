# qalx-orcaflex-examples

A set of tutorial-style examples to get started with qalx-orcaflex

## Overview

This repository contains examples of a number of different approaches to solving a very simple batch of load cases in
OrcaFlex.

All the cases are based on the Orcina provided
example [A05 Lazy wave with FPSO](https://www.orcina.com/resources/examples/?key=a#5).

For the purpose of this simplified example we will consider the waves and current coming from 8 directions and two
offset positions; near and far.

Each example shows the different features of qalx-OrcaFlex, and the different approaches that can be taken to building
batches.

## Prerequisites

These examples assume you already have a basic understanding of object-oriented Python and are familiar with using `pip`
, Python packages and virtual environments.

In addition, in order to run through the examples, you will need to have already:

- Installed `python` version >=3.8, <4.0.
- Obtained a `qalx` token from AgileTek Engineering.
- Installed and configured `qalx` as per the instructions [here](https://docs.qalx.net/#installing).

## Installing package dependencies

Create a virtual environment with:

```
python -m venv venv
```

This will keep the dependencies for this repository isolated from your global Python installed packages.

Activate the `venv` and then install the requirements for this package using:

```
pip install -r requirements.txt
```

## Starting the bots

The examples require you to start the bots by building the `qalx` factory defined in `ofx_factory.plan`.

- In a terminal/cmd window navigate to the root of this repository.
- Start the factory build process (see [here](https://docs.qalx.net/factories) for more information) with the following
  command. Use `stage-1` for examples 1 and 2; `stage-2` for example 3:

```
qalx factory-build --plan ofx_factory.plan --stage [stage-1, stage-2]
```

- At the end of the build process, if successful, you should see something like:

```
[2022-10-24 11:34:43] stage-1 - [local_sector]:    stack creation completed 
[2022-10-24 11:34:48] pyqalx:    Factory Build Successful 
```

- Additionally, you can verify that a bot has been deployed correctly
  with:

```
qalx bot-info [BatchBot, SimulationBot, RiserReportBot]
```

## Example 1

### Description

This example builds and executes an OrcaFlex batch from a set of pre-built `.dat` files, and extracts specified results
from the simulation output.

### Running

Start the factory as described above. Once the factory is running, the script is run by navigating to the `example_1`
directory and supplying the following arguments at the command line:

- Batch name
- Directory containing `.dat` files

For example, with a batch name of `test_batch` and the `.dat` files in the `data` directory as they are now:

```
python example.py test_batch data
```

This will build the batch and submit all load cases to the queue. Note that if you supply a relative path for the
directory of `.dat` files, the script assumes that it is relative to the parent `example_1` directory, however you can
also provide an absolute path.

A GUI will open to allow you to keep track of the progress by either clicking the `Get Update` button or setting the
auto-update period.

Once the batch is complete, a summary of results will be printed to the command line output.

The effective tension and curvature are pre-specified as required results.

## Example 2

### Description

This example dynamically generates a batch of load cases from one base `.dat` file by varying the direction and offset,
and extracts a set of model views from the simulation output.

### Running

Start the factory as described above. Once the factory is running, the script is run by navigating to the `example_2`
directory and supplying the following arguments at the command line:

- Batch name
- Path of base `.dat` file

For example, with a batch name of `test_batch` and the `A05 Lazy wave with FPSO.dat` file in the `example_2` directory:

```
python example.py test_batch "A05 Lazy wave with FPSO.dat"
```

This will build the batch and submit all load cases to the queue. Note that if you supply a relative path for the
base `.dat` file, the script assumes that it is relative to the parent `example_2` directory, however you can
also provide an absolute path.

A GUI will open to allow you to keep track of the progress by either clicking the `Get Update` button or setting the
auto-update period.

Once the batch is complete, a folder containing the extracted model view images will open - note that it can take up
to 1 min to summarise the results and generate the model view images after the load cases have appeared to finish
processing in the GUI.

The effective tension and curvature are pre-specified as required results.

## Example 3

### Description

This example extends example 2, by deploying another custom bot that uses the simulation output to automatically
generate a .docx report.

### Running

Start the factory as described above - remember to use `stage-2`. Once the factory is running, the script is run by
navigating to the `example_3` directory and supplying the following arguments at the command line:

- Batch name
- Path of base `.dat` file

For example, with a batch name of `test_batch` and the `A05 Lazy wave with FPSO.dat` file in the `example_3` directory:

```
python example.py test_batch "A05 Lazy wave with FPSO.dat"
```

This will build the batch and submit all load cases to the queue. Note that if you supply a relative path for the
base `.dat` file, the script assumes that it is relative to the parent `example_3` directory, however you can
also provide an absolute path.

A GUI will open to allow you to keep track of the progress by either clicking the `Get Update` button or setting the
auto-update period.

Once the batch is complete, a folder containing the extracted model view images will open - note that it can take up
to 1 min to summarise the results and generate the model view images after the load cases have appeared to finish
processing in the GUI.

The effective tension and curvature are pre-specified as required results.

Within a couple of minutes of the batch simulation completing, you should receive an email notification with a link to 
download the report generated by the `RiserReportBot`.
