from setuptools import setup, find_packages
from os.path import join, abspath, dirname

__author__ = "Gregory Halverson, Holland Hatch, Ben Jenson, Zoe von Allmen"
AUTHOR_EMAIL = "Gregory.H.Halverson@jpl.nasa.gov"
NAME = "water_rights_visualizer"
LONG_DESCRIPTION = "New Mexico Water Rights Visualizer"


def version():
    with open(join(abspath(dirname(__file__)), "water_rights_visualizer", "version.txt"), "r") as file:
        return file.read()


setup(
    name=NAME,
    version=version(),
    author=__author__,
    author_email=AUTHOR_EMAIL,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'': ["*"]}
)