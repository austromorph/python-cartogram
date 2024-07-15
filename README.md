# Compute continous cartograms (anamorphic maps)

This is a Python package to compute cartograms from `geopandas.GeoDataFrames`, using the algorithm presented in [Dougenik et al. (1985)](http://www.tandfonline.com/doi/abs/10.1111/j.0033-0124.1985.00075.x). It is the ‘sister project’ and Python implementation of our [QGIS plugin](https://github.com/austromorph/cartogram3) which continues to be available.


## Installation

`cartogram` is available from the [PyPi package
repository](https://pypi.org/project/cartogram), install it, for instance, using `pip`:

```
pip install cartogram
```


## Quick start

### Input data

You will need a polygon data set [in any format readable by
`geopandas`](https://geopandas.org/en/stable/docs/user_guide/io.html) that
features a numeric attribute column to use as the relative target values to base
the cartogram distortion on. 

If you want to have a quick try-out, see the population data for Austrian
provinces in the [`tests/data`](tests/data) directory of this repository.

### Cartogram creation

```
import cartogram
import geopandas

df = geopandas.read_file("input-data.gpkg")
c = cartogram.Cartogram(df, column="population")

c.to_file("output-data.gpkg")
```

## Documentation

Find more detailed examples and an API reference at <https://python-cartogram.readthedocs.io/>.
