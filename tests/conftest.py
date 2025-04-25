#!/usr/bin/env python3

"""Define the fixtures for unit tests."""

# This is a init file common to all tests. It is automatically sourced
# by pytest et al.

# Define common constants (e.g., paths to test data) and fixtures (e.g.,
# input dataframe) here.


import pathlib

import geopandas
import pytest


DATA_DIRECTORY = pathlib.Path(__file__).resolve().parent / "data"
AUSTRIA_NUTS2_POPULATION = DATA_DIRECTORY / "Austria_PopulationByNUTS2.geojson"
AUSTRIA_NUTS2_POPULATION_CARTOGRAM = (
    DATA_DIRECTORY / "Austria_PopulationByNUTS2_cartogram.geojson"
)

AUSTRIA_NUTS2_POPULATION_COLUMN_NAME = "pop20170101"


@pytest.fixture(scope="session")
def austria_nuts2_population_geodataframe():
    """Return a geopandas.GeoDataFrame with test data."""
    yield geopandas.read_file(AUSTRIA_NUTS2_POPULATION)


@pytest.fixture(scope="session")
def austria_nuts2_population_cartogram_geodataframe():
    """Return a geopandas.GeoDataFrame with already distorted test data."""
    yield geopandas.read_file(AUSTRIA_NUTS2_POPULATION_CARTOGRAM)


@pytest.fixture(scope="session")
def austria_nuts2_population_column_name():
    """Return the name of the cartogram column in the test data set."""
    yield AUSTRIA_NUTS2_POPULATION_COLUMN_NAME
