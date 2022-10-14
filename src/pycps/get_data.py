"""
Functions for loading CPS microdata into pandas DataFrames using the
Census API.
"""


# Key references:
# - General workings of the Census API:
#   https://www.census.gov/data/developers/guidance/microdata-api-user-guide.html
# - Easy way to check available years:
#   https://data.census.gov/mdat/#/


import os
import re

import pandas as pd  # type: ignore
import requests


# Hard code month names since they should not vary by locale
MONTH_NAME = [
    "",  # Empty string at 0 so that month number matches month name
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_asec(
    year: int,
    variables: list[str],
    show_url: bool = False,
) -> pd.DataFrame:
    """
    Load CPS ASEC microdata into a pandas DataFrame using the
    Census API.

    year: Year of data to retrieve. Years 2014 to 2022 are currently
        supported.
    variables: List of variables to retrieve.
    show_url: If True, show the URL the request was sent to. Defaults
        to False.
    """

    key = _get_key()  # Get key first to fail fast if it is not found

    _check_year_in_range(year, start_year=2014, end_year=2022)

    month = 3  # Month of CPS ASEC is always March

    url = _make_url("asec", year, month, variables, key)

    print(f"Getting CPS ASEC microdata for {year}")

    df = _get_data(url, show_url)

    return df


def get_basic(
    year: int,
    month: int,
    variables: list[str],
    show_url: bool = False,
) -> pd.DataFrame:
    """
    Load basic monthly CPS microdata into a pandas DataFrame using the
    Census API.

    year: Year of data to retrieve. Years 1989 to 2022 are currently
        supported.
    month: Month of data to retrieve (specified as a number).
    variables: List of variables to retrieve.
    show_url: If True, show the URL the request was sent to. Defaults
        to False.
    """

    key = _get_key()

    _check_year_in_range(year, start_year=1989, end_year=2022)

    url = _make_url("basic", year, month, variables, key)

    print(f"Getting basic monthly CPS microdata for {MONTH_NAME[month]} {year}")

    df = _get_data(url, show_url)

    return df


def _make_url(
    dataset: str,
    year: int,
    month: int,
    variables: list[str],
    key: str,
) -> str:
    """Create URL for Census API request."""

    _check_month(month)
    _check_variables(variables)

    month_abb = MONTH_NAME[month][:3].lower()
    vars_string = ",".join(variables).upper()

    url = (
        "https://api.census.gov/data/"
        f"{year}/cps/{dataset}/{month_abb}?get={vars_string}&key={key}"
    )

    return url


def _get_data(url: str, show_url: bool) -> pd.DataFrame:
    """Send request to URL and return response content as DataFrame."""

    if show_url:
        # Suppress key!
        print("URL:", re.sub("&key=.*", "", url))

    headers = {"user-agent": "https://github.com/matt-saenz/PyCPS"}

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise CensusAPIRequestError(
            f"Census API request failed [{resp.status_code}]: {resp.reason}"
        )

    if resp.headers["content-type"] != "application/json;charset=utf-8":
        raise CensusAPIRequestError("Census API did not return JSON")

    raw_data = resp.json()

    if not isinstance(raw_data, list):
        raise CensusAPIRequestError("Census API data not parsed as expected")

    df = _build_df(raw_data)

    return df


def _build_df(raw_data: list[list[str]]) -> pd.DataFrame:
    """Build DataFrame out of parsed response content."""

    col_names = [col_name.lower() for col_name in raw_data[0]]
    cols = raw_data[1:]

    df = pd.DataFrame(data=cols, columns=col_names)
    df = df.apply(pd.to_numeric)

    return df


def _check_year_in_range(year: int, start_year: int, end_year: int) -> None:
    """Check if year is in a simple range."""

    if year not in range(start_year, end_year + 1):
        raise ValueError(f"Years {start_year} to {end_year} are currently supported")


def _check_variables(variables: list[str]) -> None:
    """Check if variables list is valid."""

    if not isinstance(variables, list):
        raise TypeError("variables must be a list")

    not_string = [not isinstance(var, str) for var in variables]

    if any(not_string):
        raise TypeError("variables must only contain strings")

    invalid_char = [re.search("[^A-Za-z0-9_]", var) for var in variables]

    if any(invalid_char):
        raise ValueError(
            "Elements of variables must only contain letters, digits, and underscores"
        )

    if len(variables) != len(set(variables)):
        raise ValueError("variables must not contain any duplicate elements")


def _check_month(month: int) -> None:
    """Check if month is valid."""

    if not isinstance(month, int):
        raise TypeError("month must be an int")

    if month not in range(1, 13):
        raise ValueError("month must range from 1 to 12")


def _get_key() -> str:
    """Get user's Census API key."""

    key = os.getenv("CENSUS_API_KEY")

    if key is None:
        raise EnvVarNotFoundError(
            "You must provide a Census API key by setting env var CENSUS_API_KEY"
        )

    return key


# Custom exceptions


class CensusAPIRequestError(Exception):
    """Raise if something goes wrong with a Census API request."""


class EnvVarNotFoundError(Exception):
    """Raise if an environment variable is not found."""
