# PyCPS

[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

## Overview

Python rewrite of [cpsR](https://github.com/matt-saenz/cpsR), an R package I wrote for loading CPS microdata using the Census API, for learning purposes. Learning resources used include [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/), the [Python Tutorial](https://docs.python.org/3.9/tutorial/index.html), and [Beyond the Basic Stuff with Python](https://nostarch.com/beyond-basic-stuff-python).

## Setup Instructions

Start by opening your terminal and navigating to wherever you'd like to store your local clone of the repo. Once you're there, clone the repo and then move into your local clone by running:

```
git clone https://github.com/matt-saenz/PyCPS.git
cd PyCPS
```

Next, create an environment for PyCPS and then activate the environment by running:

```
conda create -n pycps_env pandas requests black mypy
conda activate pycps_env
```

Lastly, obtain a [Census API key](https://api.census.gov/data/key_signup.html) and store it in an environment variable named `CENSUS_API_KEY`.

You can verify that everything has been set up correctly and get a quick demo of the module by running:

```
python pycps.py
```

Which will allow you to calculate the employment-to-population ratio for a given month and year:

```
Hello! This if-name-main code calculates the employment-to-population (EPOP) ratio for a given month and year.
Please provide a month and year in MM/YYYY format (e.g., 09/2021): 03/2022
Getting basic monthly CPS microdata for March 2022
URL: http://api.census.gov/data/2022/cps/basic/mar?get=PRPERTYP,PRTAGE,PEMLR,PWCMPWGT
   prpertyp  prtage  pemlr   pwcmpwgt
0         2      40      1  3731.3156
1         2      35      1  4295.2243
2         2      41      7  4617.1677
3         2      42      1  5035.4937
4         1      13     -1     0.0000
5         1       9     -1     0.0000
6         2      35      1  9031.1752
7         2      66      5  1262.0923
8         2      72      5  1331.1046
9         2      85      5  1116.3924
pop16plus    263444159
employed     158105690
dtype: int64
The EPOP ratio for March 2022 was 60.0%.
```
