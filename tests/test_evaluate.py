import unittest
import numpy as np
import pandas as pd
from scripts.evaluate import COUNTERS, metrics, select_counts


class EvaluationTests(unittest.TestCase):
    def test_counter_grid_order_and_bounds(self):
        self.assertEqual(COUNTERS[0], 'count_13_n-1_13')
        self.assertEqual(COUNTERS[63], 'count_16_n-4_16')
        frame = pd.DataFrame([np.arange(64)] * 4, columns=COUNTERS)
        np.testing.assert_array_equal(select_counts(frame, [-100, 15.6, 63, 200]), [0, 16, 63, 63])

    def test_final_count_metrics_use_words(self):
        result = metrics([2, 4], [3, 2])
        self.assertEqual(result['mae_words'], 1.5)
        self.assertEqual(result['mse_words_squared'], 2.5)
        self.assertEqual(result['mean_relative_error'], 0.5)
        self.assertEqual(result['signed_bias_words'], -0.5)

    def test_invalid_reference_rejected(self):
        for reference, predictions in [([0], [1]), ([float('nan')], [1]), ([1, 2], [1])]:
            with self.assertRaises(ValueError):
                metrics(reference, predictions)


if __name__ == '__main__':
    unittest.main()
