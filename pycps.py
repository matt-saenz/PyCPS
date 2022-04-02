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

    df = _get_data(url, show_url)

    return df


def get_basic(
    year: int, month: int, vars: list[str], show_url: bool = False
) -> pd.DataFrame:
    """Get basic monthly CPS microdata using the Census API."""

    key = _get_key()

    if year not in range(1994, 2023):
        raise ValueError("Years 1994 to 2022 are currently supported")

    month_abb = _get_month_abb(month)

    formatted_vars = _format_vars(vars)

    url = f"{BASE_URL}{year}/cps/basic/{month_abb}?get={formatted_vars}&key={key}"

    df = _get_data(url, show_url)

    return df


# Helpers


def _get_data(url: str, show_url: bool) -> pd.DataFrame:
    if show_url:
        # Suppress key!
        print(re.sub("&key=.*", "", url))

    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception(
            f"Census API request failed [{resp.status_code}]: {resp.reason}"
        )

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


def _get_key() -> str:
    key = os.getenv("CENSUS_API_KEY")

    if key is None:
        raise Exception("You must set env var CENSUS_API_KEY")

    return key


def _get_month_abb(month: int) -> str:
    if month not in range(1, 13):
        raise ValueError("month must be a number ranging from 1 to 12")

    month_abbs = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]

    month_abb = month_abbs[month]

    return month_abb


if __name__ == "__main__":
    cy = int(input("Enter a year: "))
    print("Getting data...")
    asec = get_asec(cy + 1, ["marsupwt"])
    pop = asec.marsupwt.sum()
    print(f"In {cy}, the total US population was {pop:,.0f}.")
