#!/usr/bin/env python3

"""Compute continuous cartograms."""


import collections
import functools
import math

import geopandas
import joblib
import numpy
import pandas
import shapely


__all__ = ["Cartogram"]


NUM_THREADS = -1


CartogramFeature = collections.namedtuple(
    "CartogramFeature",
    [
        "cx",
        "cy",
        "mass",
        "radius",
    ],
)


class Cartogram(geopandas.GeoDataFrame):
    """Compute continuous cartograms."""

    def __init__(
        self,
        input_polygon_geodataframe,
        cartogram_attribute,
        max_iterations=10,
        max_average_error=0.1,
        verbose=False,
        **kwargs,
    ):
        """
        Compute continuous cartograms.

        This is an implementation of the Dougenik et al. (1985) algorithm to
        approximate areal cartograms from numeric data columns.
        `cartogram.Cartogram` inherits from `geopandas.GeoDataFrame`, which
        means that all methods and attributes implemented there are available in
        the result object.

        Arguments
        ---------
        input_polygon_geodataframe : geopandas.GeoDataFrame
            The input polygon data set
        cartogram_attribute : str | pandas.Series
            Which numeric attribute to use to distort the polygon data
        max_iterations : int
            How often to iterate the computation (default: 10)
        max_average_error : float
            Stop earlier than `max_iterations` if the average areal error
            reaches below `max_average_error` (a ratio between the target set by
            the attribute values and the actual area) (default: 0.1)
        """
        geopandas.GeoDataFrame.__init__(
            self, input_polygon_geodataframe.copy(), **kwargs
        )
        self.cartogram_attribute = cartogram_attribute
        self.max_iterations = max_iterations
        self.max_average_error = max_average_error
        self.verbose = verbose

        self._check_geodata()
        self._check_cartogram_attribute()

        self._transform()

    @functools.cached_property
    def area_value_ratio(self):
        """Ratio between total area and total value."""
        return self.total_area / self.total_value

    @functools.cached_property
    def average_error(self):
        """The error between the current geometries and a perfect cartogram."""
        return (
            self[[self.cartogram_attribute, "geometry"]]
            .apply(self._feature_error, axis=1)
            .mean()
            - 1
        )

    def _check_cartogram_attribute(self):
        if isinstance(self.cartogram_attribute, pandas.Series):
            cartogram_attribute_series = self.cartogram_attribute
        else:
            cartogram_attribute_series = self[self.cartogram_attribute]
        if not pandas.api.types.is_numeric_dtype(cartogram_attribute_series):
            raise ValueError("Cartogram attribute is not numeric")
        if cartogram_attribute_series.hasnans:
            raise ValueError("Cartogram attribute contains NULL values.")

    def _check_geodata(self):
        geometry_types = self.geometry.geom_type.unique().tolist()
        for geometry_type in geometry_types:
            if geometry_type not in ["MultiPolygon", "Polygon"]:
                raise ValueError(
                    f"Only POLYGON or MULTIPOLYGON geometries supported, found {geometry_type}."
                )
        self._input_is_multipolygon = "MultiPolygon" in geometry_types

    def _cartogram_feature(self, feature):
        """
        Create a cartogram feature for `polygon`.

        A cartogram feature is minimal representation of a map feature’s
        gravitational properties, following Dougenik et al. (1985).
        """
        value, polygon = feature

        centroid = polygon.centroid
        area = polygon.area
        radius = math.sqrt(area / math.pi)
        target_area = value * self.area_value_ratio
        if target_area == 0:
            mass = 0
        else:
            mass = math.sqrt(target_area / math.pi) - radius

        cartogram_feature = CartogramFeature(centroid.x, centroid.y, mass, radius)
        return cartogram_feature

    @functools.cached_property
    def _cartogram_features(self):
        """List the gravitationally active properties of all polygons."""
        return (
            self[[self.cartogram_attribute, "geometry"]]
            .apply(self._cartogram_feature, axis=1)
            .to_list()
        )

    def _feature_error(self, feature):
        """Compute the error of one feature."""
        value, geometry = feature

        area = geometry.area
        target_area = value * self.area_value_ratio

        try:
            error = max(area, target_area) / min(area, target_area)
        except ZeroDivisionError:
            print("ZeroDiv")
            error = 1.0

        return error

    def _invalidate_cached_properties(self, properties=[]):
        """Invalidate properties that were cached as `functools.cached_property`."""
        # https://stackoverflow.com/a/68316608
        if not properties:
            # # clear all as default
            # properties = [
            #     attribute
            #     for attribute in self.__dict__.keys()
            #     if isinstance(getattr(self, attribute, None), functools.cached_property)
            # ]
            properties = [
                attr
                for attr in list(self.__dict__.keys())
                if (descriptor := getattr(self.__class__, attr, None))
                if isinstance(descriptor, functools.cached_property)
            ]
        for properti in properties:
            self.__dict__.pop(properti)

    iteration = 0

    @functools.cached_property
    def _reduction_factor(self):
        """See Dougenik et al. (1985)."""
        return 1.0 / (self.average_error + 1)

    def _transform(self):
        """Transform the data set into a cartogram."""
        # TODO: - set all 0 to 0.00000001 or so (but not in output data!)
        self.geometry = self.geometry.buffer(0.0)

        self.iteration = 0
        while (
            self.iteration < self.max_iterations
            and self.average_error > self.max_average_error
        ):
            # self.geometry = self.geometry.apply(functools.partial(self._transform_geometry, features=self._cartogram_features))
            with joblib.Parallel(
                verbose=(self.verbose * 10),
                n_jobs=NUM_THREADS,
            ) as parallel:
                self.geometry = parallel(
                    joblib.delayed(
                        functools.partial(
                            self._transform_geometry,
                            features=self._cartogram_features,
                            reduction_factor=self._reduction_factor,
                        )
                    )(geometry)
                    for geometry in self.geometry
                )
            self._invalidate_cached_properties()
            self.iteration += 1
            if self.verbose:
                print(
                    f"{self.average_error:0.5f} error left after {self.iteration:d} iteration(s)"
                )

        self.geometry = self.geometry.buffer(0.0)

    def _transform_geometry(self, geometry, features, reduction_factor):
        return shapely.transform(
            geometry,
            functools.partial(
                self._transform_vertices,
                features=features,
                reduction_factor=reduction_factor,
            ),
        )

    def _transform_vertex(self, vertex, features, reduction_factor):
        x0, y0 = vertex

        x = x0
        y = y0

        for feature in features:
            if feature.mass:
                cx = feature.cx
                cy = feature.cy
                distance = math.sqrt((x0 - cx) ** 2 + (y0 - cy) ** 2)

                if distance > feature.radius:
                    # force on points ‘far away’ from the centroid
                    force = feature.mass * feature.radius / distance
                else:
                    # force on points closer to the centroid
                    dr = distance / feature.radius
                    force = feature.mass * (dr**2) * (4 - (3 * dr))
                force *= reduction_factor / distance

                x += (x0 - cx) * force
                y += (y0 - cy) * force

        # print(f"    moved vertex by {x0-x}, {y0-y}")
        return [x, y]

    def _transform_vertices(self, vertices, features, reduction_factor):
        return numpy.asarray(
            [
                self._transform_vertex(vertex, features, reduction_factor)
                for vertex in vertices
            ]
        )

    @functools.cached_property
    def total_area(self):
        """Total area of all polygons."""
        return self.geometry.area.sum()

    @functools.cached_property
    def total_value(self):
        """Sum of the values of `cartogram_attribute` over all polygons."""
        return self[self.cartogram_attribute].sum()
