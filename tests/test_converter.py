import unittest

from src.main import ConvertidorTemperatura


class TestConvertidorTemperatura(unittest.TestCase):

    def setUp(self):
        self.conv = ConvertidorTemperatura()

    # --- celsius_to_fahrenheit ---

    def test_celsius_to_fahrenheit_freezing(self):
        self.assertAlmostEqual(self.conv.celsius_to_fahrenheit(0), 32.0)

    def test_celsius_to_fahrenheit_boiling(self):
        self.assertAlmostEqual(self.conv.celsius_to_fahrenheit(100), 212.0)

    def test_celsius_to_fahrenheit_body(self):
        self.assertAlmostEqual(self.conv.celsius_to_fahrenheit(37), 98.6, places=1)

    def test_celsius_to_fahrenheit_negative(self):
        self.assertAlmostEqual(self.conv.celsius_to_fahrenheit(-40), -40.0)

    # --- fahrenheit_to_celsius ---

    def test_fahrenheit_to_celsius_freezing(self):
        self.assertAlmostEqual(self.conv.fahrenheit_to_celsius(32), 0.0)

    def test_fahrenheit_to_celsius_boiling(self):
        self.assertAlmostEqual(self.conv.fahrenheit_to_celsius(212), 100.0)

    def test_fahrenheit_to_celsius_negative(self):
        self.assertAlmostEqual(self.conv.fahrenheit_to_celsius(-40), -40.0)

    # --- celsius_to_kelvin ---

    def test_celsius_to_kelvin_zero(self):
        self.assertAlmostEqual(self.conv.celsius_to_kelvin(0), 273.15)

    def test_celsius_to_kelvin_boiling(self):
        self.assertAlmostEqual(self.conv.celsius_to_kelvin(100), 373.15)

    def test_celsius_to_kelvin_absolute_zero(self):
        self.assertAlmostEqual(self.conv.celsius_to_kelvin(-273.15), 0.0, places=1)

    # --- kelvin_to_celsius ---

    def test_kelvin_to_celsius_absolute_zero(self):
        self.assertAlmostEqual(self.conv.kelvin_to_celsius(0), -273.15)

    def test_kelvin_to_celsius_boiling(self):
        self.assertAlmostEqual(self.conv.kelvin_to_celsius(373.15), 100.0)

    def test_kelvin_to_celsius_freezing(self):
        self.assertAlmostEqual(self.conv.kelvin_to_celsius(273.15), 0.0)
