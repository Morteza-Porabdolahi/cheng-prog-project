import unittest

import app

class TestApp(unittest.TestCase):
    def test_average_velocity(self):
        # calculateAverageVelocity(volumetricFlowRate, diameter)
        self.assertAlmostEqual(app.calculateAverageVelocity(0.02, 0.1), 2.546, 2)
        self.assertAlmostEqual(app.calculateAverageVelocity(0.05, 0.25), 1.018, 2)
        self.assertAlmostEqual(app.calculateAverageVelocity(0.01, 0.05), 5.092, 2)
    def test_reynolds_num(self):
        # calculateReynolds(averageVelocity ,diameter, viscosity, density)
        self.assertAlmostEqual(app.calculateReynolds(2.546, 0.1, 0.001, 998), 254090.800, 2)
        self.assertAlmostEqual(app.calculateReynolds(1.018, 0.25, 0.001, 998), 253991, 2)
        self.assertAlmostEqual(app.calculateReynolds(5.092, 0.05, 0.001, 998), 254090.8, 2)
    def test_friction_factor(self):
        # calculateFrictionFactor(reynoldsNum, roughness, diameter)
        self.assertAlmostEqual(app.calculateFrictionFactor(254090.800, 0.000045, 0.1), 0.018, 2)
        self.assertAlmostEqual(app.calculateFrictionFactor(253991, 0.0000015, 0.25), 0.016, 2)
        self.assertAlmostEqual(app.calculateFrictionFactor(254090.800, 0.0000015, 0.05), 0.019, 2)
    def test_pressure_drop(self):
        # calculatePressureDrop(friction, length, diameter, density, averageVelocity)
        self.assertAlmostEqual(app.calculatePressureDrop(0.018, 100, 0.1, 998, 2.546), 58222.365, 2)
        self.assertAlmostEqual(app.calculatePressureDrop(0.016, 50, 0.25, 998, 1.018), 1654.802, 2)
        self.assertAlmostEqual(app.calculatePressureDrop(0.019, 2000, 0.05, 998, 5.092), 9833110.687, 2)
            

if __name__ == '__main__':
    unittest.main()
