import unittest
from data.airport_loader import load_airport_data, get_us_airports, validate_airport_code, get_airport_coordinates

class TestAirportLoader(unittest.TestCase):
    def setUp(self):
        self.airports = load_airport_data()

    def test_load_airport_data(self):
        self.assertIsInstance(self.airports, dict)
        self.assertTrue(len(self.airports) > 0)

    def test_get_us_airports(self):
        us_airports = get_us_airports(self.airports)
        self.assertTrue(all(ap.country == "United States" for ap in us_airports.values()))
        self.assertTrue(len(us_airports) > 0)

    def test_validate_airport_code(self):
        # Pick a known airport code from the loaded data
        sample_code = next(iter(self.airports.keys()))
        self.assertTrue(validate_airport_code(sample_code, self.airports))
        self.assertFalse(validate_airport_code("FAKECODE", self.airports))

    def test_get_airport_coordinates(self):
        sample_code = next(iter(self.airports.keys()))
        coords = get_airport_coordinates(sample_code, self.airports)
        self.assertIsInstance(coords, tuple)
        self.assertEqual(len(coords), 2)

if __name__ == "__main__":
    unittest.main()
