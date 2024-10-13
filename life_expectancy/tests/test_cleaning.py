# pylint: disable=line-too-long, trailing-whitespace

"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import clean_data
from . import OUTPUT_DIR

def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function for Portugal (PT) and compare the output to the expected output"""
    # Pass "PT" as the argument to clean_data
    clean_data("PT")
    
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )