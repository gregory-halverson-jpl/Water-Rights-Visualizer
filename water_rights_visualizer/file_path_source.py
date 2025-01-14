import contextlib
from datetime import date, datetime
from glob import glob
from os.path import abspath, expanduser, exists, join, isdir, basename
from typing import Union

from dateutil import parser
import logging
import cl
from .errors import FileUnavailable
from .data_source import DataSource

logger = logging.getLogger(__name__)

class FilepathSource(DataSource):
    def __init__(self, directory: str):
        """
        Initialize the FilepathSource object.

        Args:
            directory (str): The directory path where the files are located.
        
        Raises:
            IOError: If the directory does not exist.
        """
        directory = abspath(expanduser(directory))

        if not exists(directory):
            raise IOError(f"directory not found: {directory}")

        self.directory = directory

    def date_directory(self, acquisition_date: Union[date, str]) -> str:
        """
        Get the directory path for a specific acquisition date.

        Args:
            acquisition_date (Union[date, str]): The acquisition date in date or string format.
        
        Returns:
            str: The directory path for the acquisition date.
        """
        if isinstance(acquisition_date, str):
            acquisition_date = parser.parse(acquisition_date).date()

        date_directory = join(self.directory, f"{acquisition_date:%Y.%m.%d}")

        return date_directory

    def inventory(self):
        """
        Get the available years and dates in the directory.

        Returns:
            tuple: A tuple containing the list of available years and dates.
        """
        date_directory_pattern = join(self.directory, "*")
        logger.info(f"searching for date directories with pattern: {cl.val(date_directory_pattern)}")
        date_directories = sorted(glob(date_directory_pattern))
        date_directories = [directory for directory in date_directories if isdir(directory)]
        logger.info(f"found {cl.val(len(date_directories))} date directories under {cl.dir(self.directory)}")
        dates_available = [datetime.strptime(basename(directory), "%Y.%m.%d").date() for directory in date_directories]
        years_available = list(set(sorted([date_step.year for date_step in dates_available])))
        logger.info(f"counted {cl.val(len(years_available))} year available in date directories")

        return years_available, dates_available

    @contextlib.contextmanager
    def get_filename(self, tile: str, variable_name: str, acquisition_date: str) -> str:
        """
        Get the filename for a specific tile, variable, and acquisition date.

        Args:
            tile (str): The tile name.
            variable_name (str): The variable name.
            acquisition_date (str): The acquisition date in string format.
        
        Yields:
            str: The filename for the tile, variable, and acquisition date.
        
        Raises:
            FileUnavailable: If no files are found for the given parameters.
        """
        raster_directory = self.date_directory(acquisition_date)
        pattern = join(raster_directory, "**", f"*_{tile}_*_{variable_name}.tif")
        logger.info(f"searching pattern: {cl.val(pattern)}")
        matches = sorted(glob(pattern, recursive=True))

        if len(matches) == 0:
            raise FileUnavailable(
                f"no files found for tile {tile} variable {variable_name} date {acquisition_date}")

        input_filename = matches[0]
        logger.info(
            f"file for tile {cl.place(tile)} variable {cl.name(variable_name)} date {cl.time(acquisition_date)}: {cl.file(input_filename)}")

        yield input_filename
