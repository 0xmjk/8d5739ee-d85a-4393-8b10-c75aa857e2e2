#!/usr/bin/env python
import argparse
import unittest
from gethurricaneloss import _parse_arguments, get_hurricane_loss


class TestArgumentParsing(unittest.TestCase):
    def test_happy(self):
        parameters = _parse_arguments("-n", "500", "1", "2", "3", "4", "5", "6")
        expected = argparse.Namespace(
            florida_landfall_rate=1.0,
            florida_mean=2.0,
            florida_stddev=3.0,
            gulf_landfall_rate=4.0,
            gulf_mean=5.0,
            gulf_stddev=6.0,
            samples=500,
        )
        self.assertEqual(parameters, expected)


class TestModel(unittest.TestCase):
    def test_zero(self):
        num_samples = 10000
        total_loss, total_samples = get_hurricane_loss(
            0, 0, 0, 0, 0, 0, samples=num_samples
        )
        mean_loss = total_loss / total_samples
        self.assertEqual(mean_loss, 0.0)

    def test_around_five(self):
        num_samples = 10000
        total_loss, total_samples = get_hurricane_loss(
            1, 1, 0.5, 1, 0.65, 0.23, samples=num_samples
        )
        mean_loss = total_loss / total_samples
        self.assertGreater(mean_loss, 4.8)
        self.assertLess(mean_loss, 5.2)


if __name__ == "__main__":
    unittest.main()
