"""Testes das análises exploratórias."""

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from lab.eda_module import analysis


class AnalysisTests(unittest.TestCase):
    def test_descriptive_stats(self):
        df = pd.DataFrame({"rating": [80.0, 90.0, None]})
        result = analysis.descriptive_stats(df)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["mean"], 85)
        self.assertEqual(result["min"], 80)
        self.assertEqual(result["max"], 90)
        self.assertTrue({"std", "25%", "50%", "75%"}.issubset(result.index))

    def test_outliers_use_strict_iqr_bounds_and_requested_column(self):
        values = [-3, -2, 0, 1, 1, 1, 2, 2, 2, 3, 4, 6, 7, None]
        df = pd.DataFrame({"score": values, "rating": [10] * len(values)})
        original = df.copy(deep=True)

        result = analysis.detect_outliers_iqr(df, column="score")

        assert_frame_equal(result, df.iloc[[0, 12]])
        result.loc[0, "rating"] = 20
        assert_frame_equal(df, original)

    def test_missing_values_report(self):
        df = pd.DataFrame({"rating": [90, None], "variety": [None, None], "name": ["A", "B"]})
        expected = pd.Series({"rating": 1, "variety": 2, "name": 0})
        assert_series_equal(analysis.missing_values_report(df), expected)

    def test_rating_stats_by_variety(self):
        df = pd.DataFrame({"variety": ["A", "A", "B", "B"], "rating": [80, 90, 95, None]})
        expected = pd.DataFrame(
            {"count": [1, 2], "mean": [95.0, 85.0], "min": [95.0, 80.0], "max": [95.0, 90.0]},
            index=pd.Index(["B", "A"], name="variety"),
        )
        assert_frame_equal(analysis.rating_stats_by_variety(df), expected)


if __name__ == "__main__":
    unittest.main()
