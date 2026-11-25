"""Testes dos gráficos de vinhos."""

import tempfile
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pandas.testing import assert_frame_equal

from lab.viz_module import plots


class PlotTests(unittest.TestCase):
    def test_plots_save_pngs_with_expected_data_and_close_figures(self):
        df = pd.DataFrame(
            [(f"Variedade {i}", 80 + i) for i in range(12) for _ in range(12 - i)],
            columns=["variety", "rating"],
        )
        original = df.copy(deep=True)
        open_figures = plt.get_fignums()

        with tempfile.TemporaryDirectory() as directory:
            for name in ("plot_rating_distribution", "plot_top_varieties", "plot_boxplot_by_variety"):
                with self.subTest(plot=name):
                    path = Path(directory) / f"{name}.png"
                    fig = getattr(plots, name)(df, str(path))
                    ax = fig.axes[0]
                    self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                    self.assertTrue(ax.get_title() and ax.get_xlabel() and ax.get_ylabel())
                    self.assertEqual(plt.get_fignums(), open_figures)
                    if name == "plot_rating_distribution":
                        self.assertEqual(len(ax.patches), 20)
                        self.assertEqual(sum(bar.get_height() for bar in ax.patches), len(df))
                    elif name == "plot_top_varieties":
                        self.assertEqual([bar.get_width() for bar in ax.patches], list(range(3, 13)))
                        self.assertEqual(
                            {label.get_text() for label in ax.get_yticklabels()},
                            {f"Variedade {i}" for i in range(10)},
                        )
                    else:
                        self.assertEqual(
                            [label.get_text() for label in ax.get_xticklabels()],
                            [f"Variedade {i}" for i in range(5)],
                        )

        assert_frame_equal(df, original)

    def test_save_error_closes_figure(self):
        df = pd.DataFrame({"rating": [85]})
        open_figures = plt.get_fignums()
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                plots.plot_rating_distribution(df, str(Path(directory) / "missing" / "plot.png"))
        self.assertEqual(plt.get_fignums(), open_figures)


if __name__ == "__main__":
    unittest.main()
