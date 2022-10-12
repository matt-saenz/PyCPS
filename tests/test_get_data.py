"""Testing for the pycps.get_data module."""


import unittest

import pandas as pd

import pycps.get_data


class TestGetData(unittest.TestCase):
    def test_make_url(self):
        self.assertEqual(
            pycps.get_data._make_url(
                dataset="basic",
                year=2022,
                month=3,
                variables=["prtage", "pwsswgt"],
                key="helloworld1234",
            ),
            (
                # This part of URL is actually functional
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

        built = pycps.get_data._build_df(dummy_data)

        expected = pd.DataFrame(dict(hello=[1, 3], world=[2, 4]))

        self.assertTrue(built.equals(expected))
