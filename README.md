# Water Rights Visualizer

Gregory Halverson, Jet Propulsion Laboratory, [gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)

Mony Sea, California State University Northridge

Holland Hatch, Chapman University

Ben Jenson, Chapman University

Zoe von Allmen, Chapman University

This repository contains the code for the ET Toolbox 7-day hindcast and 7-day forecast data production system.

## Copyright

Copyright 2022, by the California Institute of Technology. ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged. Any commercial use must be negotiated with the Office of Technology Transfer at the California Institute of Technology.
 
This software may be subject to U.S. export control laws. By accepting this software, the user agrees to comply with all applicable U.S. export laws and regulations. User has the responsibility to obtain export licenses, or other export authority as may be required before exporting such information to foreign countries or providing access to foreign persons.

## Requirements

This system was designed to work in a Linux-like environment and macOS using a conda environment.

### `conda`

The Water Rights Visualizer is designed to run in a Python 3 [`conda`](https://docs.conda.io/en/latest/miniconda.html) environment using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) To use this environment, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Make sure that your shell has been initialized for `conda`.

You should see the base environment name `(base)` when running a shell with conda active.

## Installation

Use `make install` to produce the `water_rights` environment:

```bash
(base) $ make install
```

This should produce a conda environment called `water_rights` in your [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installation.

## Activation

To use the pipeline, you must activate the `water_rights` environment:

```bash
(base) $ conda activate water_rights
```

You should see the environment name `(water_rights)` in parentheses prepended to the command line prompt.

## Launch

To launch the Water Rights Visualizer GUI, run the `water-rights-gui` command:

```bash
(water_rights) $ water-rights-gui
```

## Deactivation

When you are done using the pipeline, you can deactivate the `water_rights` environment:

```bash
(water_rights) $ conda deactivate water_rights
```

You should see the environment name on the command line prompt change to `(base)`.

## Updating

To update your installation of the `water_rights` environment, rebuild with this command:

```bash
(base) $ make reinstall-hard
```

## Uninstallation

```bash
(base) $ make remove
```

