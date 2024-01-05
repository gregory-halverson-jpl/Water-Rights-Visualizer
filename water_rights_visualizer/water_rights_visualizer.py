#!/usr/bin/env python
# coding: utf-8
import logging
import sys
from os import makedirs, scandir
from os.path import basename, isdir, splitext
from os.path import exists, isfile
from os.path import expanduser
from pathlib import Path

import matplotlib as mpl

import cl
from .water_rights import water_rights
from .constants import *
from .data_source import DataSource
from .file_path_source import FilepathSource
from .google_source import GoogleSource

logger = logging.getLogger(__name__)

mpl.use("Agg")


def water_rights_visualizer(
        boundary_filename: str,
        output_directory: str,
        input_datastore: DataSource = None,
        input_directory: str = None,
        google_drive_temporary_directory: str = None,
        google_drive_key_filename: str = None,
        google_drive_client_secrets_filename: str = None,
        start_year: int = START_YEAR,
        end_year: int = None):
    boundary_filename = abspath(expanduser(boundary_filename))
    output_directory = abspath(expanduser(output_directory))

    if not exists(boundary_filename):
        raise IOError(f"boundary filename not found: {boundary_filename}")

    logger.info(f"boundary file: {cl.file(boundary_filename)}")

    # if isinstance(input_datastore, FilepathSource):
    #     logger.info(f"input directory: {cl.dir(input_datastore.directory)}")
    # elif isinstance(input_datastore, GoogleSource):
    #     logger.info(f"using Google Drive for input data")
    # else:
    #     raise ValueError("invalid data source")

    if input_datastore is None:
        if google_drive_temporary_directory is not None:
            input_datastore = GoogleSource(
                temporary_directory=google_drive_temporary_directory,
                key_filename=google_drive_key_filename,
                client_secrets_filename=google_drive_client_secrets_filename
            )
        elif input_directory is not None:
            input_datastore = FilepathSource(directory=input_directory)
        else:
            raise ValueError("no input data source given")

    makedirs(output_directory, exist_ok=True)
    logger.info(f"output directory: {cl.dir(output_directory)}")

    working_directory = output_directory
    # chdir(working_directory)
    logger.info(f"working directory: {cl.dir(working_directory)}")

    ROI_base = splitext(basename(boundary_filename))[0]
    DEFAULT_ROI_DIRECTORY = Path(f"{boundary_filename}")
    ROI_name = Path(f"{DEFAULT_ROI_DIRECTORY}")

    logger.info(f"target: {cl.place(ROI_name)}")

    ROI = ROI_name
    BUFFER_METERS = 2000
    # BUFFER_DEGREES = 0.001
    CELL_SIZE_DEGREES = 0.0003
    CELL_SIZE_METERS = 30
    TILE_SELECTION_BUFFER_RADIUS_DEGREES = 0.01
    ARD_TILES_FILENAME = join(abspath(dirname(__file__)), "ARD_tiles.geojson")

    if isfile(ROI):
        water_rights(
            ROI,
            input_datastore=input_datastore,
            output_directory=output_directory,
            start_year=start_year,
            end_year=end_year,
            ROI_name=None,
            figure_directory=None,
            working_directory=None,
            subset_directory=None,
            nan_subset_directory=None,
            stack_directory=None,
            monthly_sums_directory=None,
            monthly_means_directory=None,
            monthly_nan_directory=None,
            target_CRS=None)

    elif isdir(ROI):
        for items in scandir(ROI):
            if items.name.endswith(".geojson"):
                roi_name = abspath(items)
                water_rights(
                    roi_name,
                    input_datastore=input_datastore,
                    output_directory=output_directory,
                    start_year=start_year,
                    end_year=end_year,
                    ROI_name=None,
                    figure_directory=None,
                    working_directory=None,
                    subset_directory=None,
                    nan_subset_directory=None,
                    stack_directory=None,
                    monthly_sums_directory=None,
                    monthly_means_directory=None,
                    monthly_nan_directory=None,
                    target_CRS=None)
    else:
        logger.warning(f"invalid ROI: {ROI}")


def main(argv=sys.argv):
    if "--boundary-filename" in argv:
        boundary_filename = str(argv[argv.index("--boundary-filename") + 1])
    else:
        boundary_filename = None

    if "--output-directory" in argv:
        output_directory = str(argv[argv.index("--output-directory") + 1])
    else:
        output_directory = None

    if "--input-directory" in argv:
        input_directory = str(argv[argv.index("--input-directory") + 1])
    else:
        input_directory = None

    if "--google-drive-temporary-directory" in argv:
        google_drive_temporary_directory = str(argv[argv.index("--google-drive-temporary-directory") + 1])
    else:
        google_drive_temporary_directory = None

    if "--google-drive-key-filename" in argv:
        google_drive_key_filename = str(argv[argv.index("--google-drive-key-filename") + 1])
    else:
        google_drive_key_filename = None

    if "--google-drive-client-secrets-filename" in argv:
        google_drive_client_secrets_filename = str(argv[argv.index("--google-drive-client-secrets-filename") + 1])
    else:
        google_drive_client_secrets_filename = None

    water_rights_visualizer(
        boundary_filename=boundary_filename,
        output_directory=output_directory,
        input_directory=input_directory,
        google_drive_temporary_directory=google_drive_temporary_directory,
        google_drive_key_filename=google_drive_key_filename,
        google_drive_client_secrets_filename=google_drive_client_secrets_filename
    )


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv))
