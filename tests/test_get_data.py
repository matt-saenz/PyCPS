"""Testing for the pycps.get_data module."""


import unittest

import pandas as pd  # type: ignore

import pycps.get_data as get_data


class TestGetData(unittest.TestCase):
    def test_check_variables(self):
        self.assertIsNone(get_data._check_variables(["HELLO_world_1234"]))

        bad_types = ["hello", ["hello", 1]]

        for bad_type in bad_types:
            with self.assertRaises(TypeError):
                get_data._check_variables(bad_type)

        bad_vals = [["hello, world?"], ["hello", "hello"]]

        for bad_val in bad_vals:
            with self.assertRaises(ValueError):
                get_data._check_variables(bad_val)

    def test_make_url(self):
        self.assertEqual(
            get_data._make_url(
                dataset="basic",
                year=2022,
                month=3,
                variables=["prtage", "pwsswgt"],
                key="helloworld1234",
            ),
            (
                # This part of the URL is actually functional
                "https://api.census.gov/data/2022/cps/basic/mar?get=PRTAGE,PWSSWGT"
                # This part causes failure because of invalid key (as you'd expect)
                "&key=helloworld1234"
            ),
        )

    def test_build_df(self):
        dummy_data = [["HELLO", "WORLD"], ["1", "2"], ["3", "4"]]
        # [["HELLO", "WORLD"],
        # ["1", "2"],
        # ["3", "4"]]

        built = get_data._build_df(dummy_data)

        expected = pd.DataFrame(dict(hello=[1, 3], world=[2, 4]))

        self.assertTrue(built.equals(expected))

    def test_check_year_in_range(self):
        start_year, end_year = 2010, 2013

        for year in range(start_year, end_year + 1):
            self.assertIsNone(get_data._check_year_in_range(year, start_year, end_year))

        for bad_year in [start_year - 1, end_year + 1]:
            with self.assertRaises(ValueError):
                get_data._check_year_in_range(bad_year, start_year, end_year)

    def test_check_month(self):
        for month in range(1, 13):
            self.assertIsNone(get_data._check_month(month))

        for bad_month in [0, 13]:
            with self.assertRaises(ValueError):
                get_data._check_month(bad_month)


if __name__ == "__main__":
    unittest.main()
