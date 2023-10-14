# PyCPS

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Downloads](https://static.pepy.tech/badge/pycpsdata)](https://pepy.tech/project/pycpsdata)

## Overview

Python package for loading [Current Population Survey (CPS)](https://www.census.gov/programs-surveys/cps/about.html) microdata into a [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) using the Census Bureau Data API, including [basic monthly CPS](https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html) and [CPS ASEC](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.html) microdata.

Note: This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.

For an R version of this package, check out [cpsR](https://github.com/matt-saenz/cpsR).

## Setup Instructions

Install the package:

```shell
pip install pycpsdata  # Alas, pycps was taken
```

and store your [Census API key](https://api.census.gov/data/key_signup.html) in an environment variable named `CENSUS_API_KEY`.

## Example Usage

```python
from pycps import get_asec

asec = get_asec(2021, ["a_age", "marsupwt"])

asec
#         a_age  marsupwt
# 0          56    687.71
# 1          57    687.71
# 2          78    646.86
# 3          65   1516.95
# 4          66   1516.95
# ...       ...       ...
# 163538     69    514.11
# 163539     70    516.25
# 163540     66    516.25
# 163541     55    386.37
# 163542     52    386.37
#
# [163543 rows x 2 columns]

asec.marsupwt.sum()
# 326195439.67
```
