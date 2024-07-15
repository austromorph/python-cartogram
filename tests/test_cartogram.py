#!/usr/bin/env python3


import geopandas.testing
import pytest
import pytest_lazy_fixtures

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
            )
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
