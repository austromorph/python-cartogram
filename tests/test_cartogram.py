#!/usr/bin/env python3


import geopandas.testing
import pytest
import pytest_lazy_fixtures
import shapely

import cartogram


class TestCartogram:
    @pytest.mark.parametrize(
        [
            "input_geodataframe",
            "column_name",
            "expected_result_geodataframe",
        ],
        [
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_population_column_name"),
                pytest_lazy_fixtures.lf(
                    "austria_nuts2_population_cartogram_geodataframe"
                ),
            ),
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_population_column"),
                pytest_lazy_fixtures.lf(
                    "austria_nuts2_population_cartogram_geodataframe"
                ),
            ),
        ],
    )
    def test_cartogram(
        self,
        input_geodataframe,
        column_name,
        expected_result_geodataframe,
    ):
        geopandas.testing.assert_geodataframe_equal(
            cartogram.Cartogram(input_geodataframe, column_name),
            expected_result_geodataframe,
            check_like=True,
            check_less_precise=True,
            normalize=True,
        )

    @pytest.mark.parametrize(
        [
            "input_geodataframe",
            "column_name",
            "expected_result_geodataframe",
        ],
        [
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_population_column_name"),
                pytest_lazy_fixtures.lf(
                    "austria_nuts2_population_cartogram_geodataframe"
                ),
            ),
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_population_column"),
                pytest_lazy_fixtures.lf(
                    "austria_nuts2_population_cartogram_geodataframe"
                ),
            ),
        ],
    )
    def test_cartogram_verbose(
        self,
        input_geodataframe,
        column_name,
        expected_result_geodataframe,
    ):
        geopandas.testing.assert_geodataframe_equal(
            cartogram.Cartogram(input_geodataframe, column_name, verbose=True),
            expected_result_geodataframe,
            check_like=True,
            check_less_precise=True,
            normalize=True,
        )

    def test_cartogram_with_pandas_series(
        self,
        austria_nuts2_population_geodataframe,
        austria_nuts2_population_column_name,
        austria_nuts2_population_cartogram_geodataframe,
    ):
        geopandas.testing.assert_geodataframe_equal(
            cartogram.Cartogram(
                austria_nuts2_population_geodataframe,
                austria_nuts2_population_geodataframe[
                    austria_nuts2_population_column_name
                ],
            ),
            austria_nuts2_population_cartogram_geodataframe,
            check_like=True,
            check_less_precise=True,
            normalize=True,
        )

    @pytest.mark.parametrize(
        [
            "input_geodataframe",
            "column_name",
        ],
        [
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_nonnumeric_column_name"),
            ),
            (
                pytest_lazy_fixtures.lf("austria_nuts2_population_geodataframe"),
                pytest_lazy_fixtures.lf("austria_nuts2_nonnumeric_column"),
            ),
        ],
    )
    def test_cartogram_non_numeric(
        self,
        input_geodataframe,
        column_name,
    ):
        with pytest.raises(ValueError, match="Cartogram attribute is not numeric"):
            _ = (cartogram.Cartogram(input_geodataframe, column_name),)

    def test_cartogram_null_values(
        self,
        austria_nuts2_population_geodataframe,
        austria_nuts2_population_column_name,
    ):
        austria_nuts2_population_geodataframe.at[
            1, austria_nuts2_population_column_name
        ] = None
        with pytest.raises(
            ValueError, match="Cartogram attribute contains NULL values"
        ):
            _ = cartogram.Cartogram(
                austria_nuts2_population_geodataframe,
                austria_nuts2_population_column_name,
            )

    def test_cartogram_other_geometries(
        self,
        austria_nuts2_population_geodataframe,
        austria_nuts2_population_column_name,
    ):
        austria_nuts2_population_geodataframe["geometry"] = shapely.Point()
        with pytest.raises(
            ValueError, match="Only POLYGON or MULTIPOLYGON geometries supported"
        ):
            _ = cartogram.Cartogram(
                austria_nuts2_population_geodataframe,
                austria_nuts2_population_column_name,
            )
