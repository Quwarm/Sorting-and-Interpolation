import unittest
from lagrange_interpolation import interpolation_formula
from decimal import Decimal, getcontext

MAX_ACCURACY = 6
MIN_NUMBER = -1000
MAX_NUMBER = +1000
MAX_SIZE = 50
getcontext().prec = 1000


class LagrangeInterpolationTest(unittest.TestCase):

    def test_sample(self):
        global MAX_ACCURACY
        self.assertEqual(interpolation_formula([], [], 0), '+0*x^0')
        for i in range(1, MAX_ACCURACY + 1):
            self.assertEqual(interpolation_formula([], [], i), '+0.' + ('0' * i) + '*x^0')
        self.assertEqual(interpolation_formula([1, 2, 3], [1, 4, 9], 0), '+1*x^2')
        self.assertEqual(interpolation_formula([1, 2, 3], [1, 4, 9], 2), '+1.00*x^2')
        self.assertEqual(interpolation_formula([1, 2, 3], [1, 4, 9], 4), '+1.0000*x^2')
        self.assertEqual(interpolation_formula([1, 2, 3], [1, 4, 9], 6), '+1.000000*x^2')
        self.assertEqual(
            interpolation_formula([-1.5, -0.75, 0, 0.75, 1.5], [-14.1014, -0.931596, 0, 0.931596, 14.1014], 0),
            '-1*x^1 +5*x^3')
        self.assertEqual(
            interpolation_formula([-1.5, -0.75, 0, 0.75, 1.5], [-14.1014, -0.931596, 0, 0.931596, 14.1014], 2),
            '-1.48*x^1 +4.83*x^3')
        self.assertEqual(
            interpolation_formula([-1.5, -0.75, 0, 0.75, 1.5], [-14.1014, -0.931596, 0, 0.931596, 14.1014], 4),
            '-1.4775*x^1 +4.8348*x^3')
        self.assertEqual(
            interpolation_formula([-1.5, -0.75, 0, 0.75, 1.5], [-14.1014, -0.931596, 0, 0.931596, 14.1014], 6),
            '-1.477474*x^1 +4.834848*x^3')

    def test_complex(self):
        global MIN_NUMBER, MAX_NUMBER, MAX_SIZE, MAX_ACCURACY
        output_format = '{:+.' + str(MAX_ACCURACY) + 'f}*x^{}'

        start, stop = MIN_NUMBER, MIN_NUMBER + MAX_SIZE
        x = [Decimal(start + i * (stop - start) / MAX_SIZE) for i in range(MAX_SIZE)]
        y = [Decimal(MAX_NUMBER) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY), output_format.format(MAX_NUMBER, 0))
        y = [Decimal(MIN_NUMBER) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY), output_format.format(MIN_NUMBER, 0))

        start, stop = MAX_NUMBER - MAX_SIZE, MAX_NUMBER
        x = [Decimal(start + i * (stop - start) / MAX_SIZE) for i in range(MAX_SIZE)]
        y = [Decimal(MAX_NUMBER) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY), output_format.format(MAX_NUMBER, 0))
        y = [Decimal(MIN_NUMBER) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY), output_format.format(MIN_NUMBER, 0))

        start, stop = MIN_NUMBER, MIN_NUMBER + MAX_SIZE / (10 ** MAX_ACCURACY)
        x = [Decimal(start + i * (stop - start) / MAX_SIZE) for i in range(MAX_SIZE)]
        y = [Decimal(MAX_NUMBER - 10 ** (-MAX_ACCURACY)) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY),
                         output_format.format(MAX_NUMBER - 10 ** (-MAX_ACCURACY), 0))
        y = [Decimal(MIN_NUMBER + 10 ** (-MAX_ACCURACY)) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY),
                         output_format.format(MIN_NUMBER + 10 ** (-MAX_ACCURACY), 0))

        start, stop = MAX_NUMBER - MAX_SIZE / (10 ** MAX_ACCURACY), MAX_NUMBER
        x = [Decimal(start + i * (stop - start) / MAX_SIZE) for i in range(MAX_SIZE)]
        y = [Decimal(MAX_NUMBER - 10 ** (-MAX_ACCURACY)) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY),
                         output_format.format(MAX_NUMBER - 10 ** (-MAX_ACCURACY), 0))
        y = [Decimal(MIN_NUMBER + 10 ** (-MAX_ACCURACY)) for i in range(MAX_SIZE)]
        self.assertEqual(interpolation_formula(x, y, MAX_ACCURACY),
                         output_format.format(MIN_NUMBER + 10 ** (-MAX_ACCURACY), 0))


if __name__ == '__main__':
    unittest.main()
