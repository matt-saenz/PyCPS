import os
import re

import pandas as pd  # type: ignore
import requests


BASE_URL = "http://api.census.gov/data/"


# Core functions


def get_asec(year: int, vars: list[str], show_url: bool = False) -> pd.DataFrame:
    """Get CPS ASEC microdata using the Census API."""

    key = _get_key()

    if year not in range(2014, 2022):
        raise ValueError("Years 2014 to 2021 are currently supported")

    formatted_vars = _format_vars(vars)

    url = f"{BASE_URL}{year}/cps/asec/mar?get={formatted_vars}&key={key}"

    print(f"Getting CPS ASEC microdata for {year}")

    df = _get_data(url, show_url)

    return df


def get_basic(
    year: int, month: int, vars: list[str], show_url: bool = False
) -> pd.DataFrame:
    """Get basic monthly CPS microdata using the Census API."""

    key = _get_key()

    if year not in range(1994, 2023):
        raise ValueError("Years 1994 to 2022 are currently supported")

    month_name, month_abb = _get_month_info(month)

    formatted_vars = _format_vars(vars)

    url = f"{BASE_URL}{year}/cps/basic/{month_abb}?get={formatted_vars}&key={key}"

    print(f"Getting basic monthly CPS microdata for {month_name} {year}")

    df = _get_data(url, show_url)

    return df


# Helpers


class CensusAPIRequestError(Exception):
    """Raise if Census API request fails."""


def _get_data(url: str, show_url: bool) -> pd.DataFrame:
    if show_url:
        # Suppress key!
        print("URL:", re.sub("&key=.*", "", url))

    resp = requests.get(url)

    if resp.status_code != 200:
        raise CensusAPIRequestError(
            f"Census API request failed [{resp.status_code}]: {resp.reason}"
        )

    if resp.headers["content-type"] != "application/json;charset=utf-8":
        raise CensusAPIRequestError("Census API did not return JSON")

    df = pd.DataFrame(resp.json())

    df.columns = df.iloc[0].str.lower().to_list()
    df = df.iloc[1:].reset_index(drop=True)
    df = df.apply(pd.to_numeric)

    return df


def _format_vars(vars: list[str]) -> str:
    if not isinstance(vars, list):
        raise TypeError("vars must be a list")

    not_string = [not isinstance(var, str) for var in vars]

    if any(not_string):
        raise TypeError("vars must only contain strings")

    invalid_char = [bool(re.search("[^A-Za-z0-9_]", var)) for var in vars]

    if any(invalid_char):
        raise ValueError(
            "Elements of vars must only contain letters, digits, and underscores"
        )

    formatted_vars = ",".join(vars).upper()

    return formatted_vars


# Create custom exception since clear built-in does not exist
class EnvVarNotFoundError(Exception):
    """Raise if environment variable is not found."""


def _get_key() -> str:
    key = os.getenv("CENSUS_API_KEY")

    if key is None:
        raise EnvVarNotFoundError(
            "You must provide a Census API key by setting env var CENSUS_API_KEY"
        )

    return key


def _get_month_info(month: int) -> tuple[str, str]:
    if month not in range(1, 13):
        raise ValueError("month must be a number ranging from 1 to 12")

    month_info_lookup = {
        1: ("January", "jan"),
        2: ("February", "feb"),
        3: ("March", "mar"),
        4: ("April", "apr"),
        5: ("May", "may"),
        6: ("June", "jun"),
        7: ("July", "jul"),
        8: ("August", "aug"),
        9: ("September", "sep"),
        10: ("October", "oct"),
        11: ("November", "nov"),
        12: ("December", "dec"),
    }

    month_info = month_info_lookup[month]

    return month_info


if __name__ == "__main__":
    # Get inputs
    print(
        "Hello! This if-name-main code calculates the employment-to-population "
        "(EPOP) ratio for a given month and year."
    )
    month_year = input(
        "Please provide a month and year in MM/YYYY format (e.g., 09/2021): "
    )
    month, year = [int(x) for x in month_year.split("/")]
    month_name, month_abb = _get_month_info(month)
    # Get data
    cps = get_basic(year, month, ["prpertyp", "prtage", "pemlr", "pwcmpwgt"], True)
    print(cps.head(10))
    # Clean data
    cps = cps.loc[(cps.prpertyp == 2) & (cps.prtage >= 16)]
    cps["pop16plus"] = True  # Given above filter
    cps["employed"] = cps.pemlr.isin([1, 2])
    # Analyze data
    results = (
        cps[["pop16plus", "employed"]]
        .apply(lambda x, wt: x.dot(wt), wt=cps.pwcmpwgt)  # Weighted sum
        .astype(int)
    )
    print(results)
    # Calculate EPOP ratio
    print(
        f"The EPOP ratio for {month_name} {year} was "
        f"{results['employed'] / results['pop16plus']:.1%}."
    )
