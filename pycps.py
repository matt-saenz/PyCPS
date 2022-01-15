

import re
import os
import requests
import pandas as pd


# Core functions

def get_asec(year: int, vars: list, show_url: bool = False) -> pd.DataFrame:
    """Get CPS ASEC microdata using the Census API."""

    key = _get_key()

    if year not in range(2014, 2022):
        raise ValueError('Years 2014 to 2021 are currently supported')

    vars = _format_vars(vars)

    url = (
        'http://api.census.gov/data/'
        f'{year}/cps/asec/mar?get={vars}&key={key}'
    )

    df = _get_data(url, show_url)

    return df


def get_basic(
    year: int,
    month: int,
    vars: list,
    show_url: bool = False
) -> pd.DataFrame:
    """Get basic monthly CPS microdata using the Census API."""

    key = _get_key()

    if year not in range(1994, 2022):
        raise ValueError('Years 1994 to 2021 are currently supported')

    month_abb = _get_month_abb(month)

    vars = _format_vars(vars)

    url = (
        'http://api.census.gov/data/'
        f'{year}/cps/basic/{month_abb}?get={vars}&key={key}'
    )

    df = _get_data(url, show_url)

    return df


# Helpers

def _get_data(url: str, show_url: bool) -> pd.DataFrame:
    if show_url:
        # Suppress key!
        print(re.sub('&key=.*', '', url))

    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception(
            f'Census API request failed [{resp.status_code}]: {resp.reason}'
        )

    df = pd.DataFrame(resp.json())

    df.columns = df.iloc[0].str.lower().to_list()
    df = df.iloc[1:].reset_index(drop = True)
    df = df.apply(pd.to_numeric)

    return df


def _format_vars(vars: list) -> str:
    if not isinstance(vars, list):
        raise TypeError('vars must be a list')

    match = [bool(re.search('[^A-Za-z0-9_]', var)) for var in vars]

    if any(match):
        raise ValueError(
            'vars must only contain letters, digits, and underscores'
        )

    vars = ','.join(vars).upper()

    return vars


def _get_key() -> str:
    key = os.getenv('CENSUS_API_KEY')

    if key is None:
        raise Exception('You must set env var CENSUS_API_KEY')

    return key


def _get_month_abb(month: int) -> str:
    if month not in range(1, 13):
        raise ValueError('month must be a number ranging from 1 to 12')

    month_abbs = [
        '', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
        'oct', 'nov', 'dec'
    ]

    month_abb = month_abbs[month]

    return month_abb


if __name__ == '__main__':
    cy = int(input('Enter a year: '))
    print('Getting data...')
    asec = get_asec(cy + 1, ['marsupwt'])
    pop = asec.marsupwt.sum()
    print(f'In {cy}, the total US population was {pop:,.0f}.')
