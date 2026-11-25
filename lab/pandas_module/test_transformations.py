"""Testes das transformações de vinhos."""

import tempfile
import unittest
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from lab.pandas_module import transformations as T


class TransformationsTests(unittest.TestCase):
    def test_load_wines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wines.csv"
            path.write_text("name,rating\nWine,90\n", encoding="utf-8")
            result = T.load_wines(str(path))

        assert_frame_equal(result, pd.DataFrame({"name": ["Wine"], "rating": [90]}))

    def test_clean_ratings_and_top_varieties(self):
        source = pd.DataFrame(
            {
                "variety": ["A", "A", "B", "C", "C"],
                "rating": ["80", "90", "95", "inválido", None],
            }
        )
        original = source.copy(deep=True)

        cleaned = T.clean_ratings(source)
        result = T.top_varieties_by_avg_rating(cleaned, n=1)

        self.assertEqual(cleaned["rating"].tolist(), [80.0, 90.0, 95.0])
        assert_frame_equal(result, pd.DataFrame({"variety": ["B"], "avg_rating": [95.0]}))
        assert_frame_equal(source, original)

    def test_rating_categories_include_boundaries_and_preserve_nulls(self):
        source = pd.DataFrame({"rating": [84.9, 85.0, 90.0, 90.1, None]})
        original = source.copy(deep=True)

        result = T.add_rating_category(source)

        self.assertEqual(result["rating_category"].iloc[:4].tolist(), ["Baixa", "Média", "Média", "Alta"])
        self.assertTrue(pd.isna(result["rating_category"].iloc[4]))
        assert_frame_equal(source, original)

    def test_country_uses_last_segment_and_preserves_nulls(self):
        source = pd.DataFrame({"region": ["Mendocino, California", "A, B, C ", " Portugal ", None]})
        original = source.copy(deep=True)

        result = T.enrich_with_country(source)

        self.assertEqual(result["country"].iloc[:3].tolist(), ["California", "C", "Portugal"])
        self.assertTrue(pd.isna(result["country"].iloc[3]))
        assert_frame_equal(source, original)


if __name__ == "__main__":
    unittest.main()
