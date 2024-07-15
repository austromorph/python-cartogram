# *python-cartogram* - compute continuous cartograms


:::{thumbnail} _static/images/Austria_PopulationCartogram_NUTS2_20170101.png
:alt: A map showing the nine federal provinces of Austria, distorted in a way that their relative areas relate to their population numbers.
:title: The nine federal provinces of Austria, distorted so their area sizes match their population numbers
:show_caption: 1
:class: align-default
:::


**python-cartogram** is a Python package that can be used to compute continuous
cartograms. These map-like cartographic visualisations, also known as
*anamorphic maps*, show areal features distorted by an attribute value, for
instance census tracts resized by population size, or election districts by
voter counts.

The package is modelled after the [QGIS plugin
*cartogram3*](https://github.com/austromorph/cartogram3). Just like it,
**python-cartogram** implements the iterative, approximating algorithm by
{cite:t}`dougenik_1985`, but it is designed to seamlessly interact with
{class}`geopandas.GeoDataFrame`s.

:::{toctree}
:caption: User guide
:maxdepth: 1
:hidden:

User manual <user-guide/user-manual/quickstart>
user-guide/installation/installation
user-guide/citation
:::

:::{toctree}
:caption: API reference
:maxdepth: 1
:hidden:

Module contents <reference/reference>
:::

:::{bibliography}
:filter: docname in docnames
:::
