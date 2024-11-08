import unittest

app = __import__('app')

class TestApp(unittest.TestCase):
    def test_average_velocity(self):
        self.assertAlmostEqual(app.calculateAverageVelocity(0.02, 0.1), 2.546, 2)
        self.assertAlmostEqual(app.calculateAverageVelocity(0.05, 0.25), 1.018, 2)
        self.assertAlmostEqual(app.calculateAverageVelocity(0.01, 0.05), 5.092, 2)
    def test_reynolds_num(self):
        self.assertAlmostEqual(app.calculateReynolds(2.546, 0.1, 0.001, 998), 254090.800 , 2)
        self.assertAlmostEqual(app.calculateReynolds(1.018, 0.25, 0.001, 998), 253991, 2)
        self.assertAlmostEqual(app.calculateReynolds(5.092, 0.05, 0.001, 998), 254090.8, 2)

if __name__ == '__main__':
    unittest.main()
        

