import unittest
import src.backend.core.bmi_calculator as bmi_calc
import src.backend.core.bmi_per_city as bmi_per_city
import src.backend.core.bmi_per_state as bmi_per_state

class TestBMICalculator(unittest.TestCase):
    def test_bmi_calculator(self):
        self.assertAlmostEqual(bmi_calc.bmi_calculator(70, 175), 22.86, places=2)
        self.assertAlmostEqual(bmi_calc.bmi_calculator(50, 160), 19.53, places=2)
        self.assertAlmostEqual(bmi_calc.bmi_calculator(90, 180), 27.78, places=2)

    def test_get_bmi_category(self):
        self.assertEqual(bmi_calc.get_bmi_category(18.5), "underweight")
        self.assertEqual(bmi_calc.get_bmi_category(22.0), "normal")
        self.assertEqual(bmi_calc.get_bmi_category(27.0), "overweight")
        self.assertEqual(bmi_calc.get_bmi_category(32.0), "obese")

class TestBMIPerCity(unittest.TestCase):
    def test_bmi_per_city(self):
        bmi_dict = bmi_per_city.get_bmi_per_city()
        self.assertIsInstance(bmi_dict, dict)
        for city, bmi in bmi_dict.items():
            self.assertIsInstance(city, str)
            self.assertIsInstance(bmi, float)

def test_bmi_per_state(self):
        bmi_dict = bmi_per_state.get_bmi_per_state()
        self.assertIsInstance(bmi_dict, dict)
        for state, bmi in bmi_dict.items():
            self.assertIsInstance(state, str)
            self.assertIsInstance(bmi, float)
        

if __name__ == '__main__':
    unittest.main()