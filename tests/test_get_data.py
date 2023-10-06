"""Testing for the pycps.get_data module."""


from typing import Any

import pandas as pd  # type: ignore
import pytest

from pycps import get_data


class TestCheckVariables:
    def test_pass(self) -> None:
        get_data._check_variables(["column", "COLUMN_2", "3_last_column"])

    @pytest.mark.parametrize(
        "bad_type",
        [
            "column",
            ["column", 1],
        ],
    )
    def test_bad_type(self, bad_type: Any) -> None:
        with pytest.raises(TypeError):
            get_data._check_variables(bad_type)

    @pytest.mark.parametrize(
        "bad_value",
        [
            ["a column"],
            ["column?"],
            ["column", "column"],
            ["column", "COLUMN"],
            ["some_column,another_column"],
        ],
    )
    def test_bad_value(self, bad_value: list[str]) -> None:
        with pytest.raises(ValueError):
            get_data._check_variables(bad_value)


def test_make_url() -> None:
    actual = get_data._make_url(
        dataset="basic",
        year=2022,
        month=3,
        variables=["prtage", "pwsswgt"],
        key="1234",
    )

    expected = (
        # This technically works, although package users must set API key
        "https://api.census.gov/data/2022/cps/basic/mar?get=PRTAGE,PWSSWGT"
        # Fake key, breaks the above
        "&key=1234"
    )

    assert actual == expected


@pytest.mark.parametrize(
    "raw_data,expected_df",
    [
        (
            # All columns parsable as numeric
            [
                ["SOME_COLUMN", "ANOTHER_COLUMN"],
                ["9", "7.3"],
                ["5", "1.4"],
            ],
            pd.DataFrame(
                {
                    "some_column": [9, 5],
                    "another_column": [7.3, 1.4],
                }
            ),
        ),
        (
            # One column not parsable as numeric
            # Should remain a string
            [
                ["SOME_COLUMN", "ANOTHER_COLUMN", "STRING_COLUMN"],
                ["9", "7.3", "a"],
                ["5", "1.4", "b"],
            ],
            pd.DataFrame(
                {
                    "some_column": [9, 5],
                    "another_column": [7.3, 1.4],
                    "string_column": ["a", "b"],
                }
            ),
        ),
    ],
)
def test_build_df(
    raw_data: list[list[str]],
    expected_df: pd.DataFrame,
) -> None:
    actual_df = get_data._build_df(raw_data)

    pd.testing.assert_frame_equal(actual_df, expected_df)


class TestCheckYear:
    @pytest.mark.parametrize("year", [2000, 2001])
    def test_pass(self, year: int) -> None:
        get_data._check_year(year, min_year=2000)

    def test_fail(self) -> None:
        with pytest.raises(ValueError):
            get_data._check_year(1999, min_year=2000)


class TestCheckMonth:
    @pytest.mark.parametrize(
        "valid_month",
        range(1, 13),
    )
    def test_pass(self, valid_month: int) -> None:
        get_data._check_month(valid_month)

    @pytest.mark.parametrize(
        "bad_value",
        [0, 13],
    )
    def test_bad_value(self, bad_value: int) -> None:
        with pytest.raises(ValueError):
            get_data._check_month(bad_value)

    def test_bad_type(self) -> None:
        with pytest.raises(TypeError):
            get_data._check_month("jan")  # type: ignore
