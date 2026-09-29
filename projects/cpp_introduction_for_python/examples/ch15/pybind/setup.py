from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

setup(
    name="example",
    ext_modules=[Pybind11Extension("example", ["example.cpp"])],
)
