---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell}
:tags: [remove-input, remove-output]

# this cell is hidden from READTHEDOCS output
# it’s used to set DATA_DIRECTORY

import pathlib
DATA_DIRECTORY = pathlib.Path().resolve() / "_static" / "data"
```

# Quickstart

Start with a {class}`GeoDataFrame<geopandas.GeoDataFrame>` of a polygon data set
that has a column with attribute values referring to absolute numbers of an
occurrence, for instance the population of counties or the voter counts in
election districts.

For this example, we prepared a sample data set that you can also download from
the [GitHub repository](https://github.com/austromorph/python-cartogram/).
This data set contains polygons showing the nine federal provinces of Austria,
with population numbers attached in a column called `pop20170101`.

% TODO: Add direct URL (not yet possible as smashed PR will change commit
% hashes)

```{code-cell}
import geopandas
df = geopandas.read_file(DATA_DIRECTORY / "Austria_PopulationByNUTS2.geojson")
df
```

```{code-cell}
df.explore(column="pop20170101", cmap="Reds")
```

As you can clearly see, population numbers diverge greatly. Vienna (AT13), the capital,
has the highest population with almost 2 million inhabitants, while it has the
smallest surface area. By contrast, Carinthia (AT21) and Tyrol (AT33), in the South and
Western parts of the country, have small populations spread over a large surface
area.

Let’s resize the polygons so that the relative surface area is representative of
the relative population of each province, by initialising a new instance of 
{class}`Cartogram<cartogram.Cartogram>`, passing a column name: 

```{code-cell}
import cartogram

c = cartogram.Cartogram(df, "pop20170101")
c
```

```{code-cell}
c.explore()
```

{class}`cartogram.Cartogram` inherits from {class}`geopandas.GeoDataFrame`, so
all of the latter’s methods and attributes are available in the result
dataframe. For instance, to save the output data set to a new file, just use
{meth}`to_file()<geopandas.GeoDataFrame.to_file>`:

```{code-cell}
c.to_file(DATA_DIRECTORY / "cartogram.geojson")
```

```{code-cell}
:tags: [remove-input, remove-output]

# this cell is hidden from READTHEDOCS output
# it’s used to prevent the output file from ever leaking into git

import os
os.unlink(DATA_DIRECTORY / "cartogram.geojson")
```


## Fine-tuning the distortions

The algorithm implemented in *python-cartogram* is an approximating, iterative
approach that was first presented by {cite:t}`dougenik_1985`, and is also used
by the [QGIS plugin cartogram3](https://github.com/austromorph/cartogram3).

Because of its iterative design, the computation becomes more precise with every
repetition. This, in turn, means longer computation times. You can control the
accuracy of the output data set using two parameters, overriding their default
values: the maximum number of iterations, and the desired average areal error
remaining in the output. The two are complimentary: if the remaining average
error is lower than the specified threshold before `max_iterations` is reached,
the remaining iterations are skipped.

```{code-cell}
c = cartogram.Cartogram(
    df,
    "pop20170101",
    max_iterations=99,
    max_average_error=0.05,
)
```

:::{admonition} Average residual area error
:class: hint

The remaining error is stored in an attribute of a cartogram:
{attr}`cartogram.Cartogram.average_error`
:::

```{code-cell}
c.average_error
```


## References

:::{bibliography}
:::
