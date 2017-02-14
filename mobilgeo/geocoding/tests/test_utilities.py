import unittest

import numpy as np
from mobilgeo.geocoding.utility import argsort_coords


A = np.array([[0.3533399, -0.35780151],
              [-2.08578735, 2.02264973],
              [-0.84677, 0.296875],
              [0.24095529, -0.29138685],
              [2.22473644, -1.37972674],
              [-0.08389701, 0.20326198],
              [1.0755367, -0.30688856],
              [1.12693161, -0.78996946],
              [-1.87464081, 1.32235628],
              [-1.5, 0.5]])

args = [1, 8, 9, 2, 5, 3, 0, 6, 7, 4]


class TestUtilities(unittest.TestCase):

    def test_argsort_coords(self):
        output = argsort_coords(A, start_index=1)
        self.assertEqual(output, args)


if __name__ == '__main__':
    unittest.main()
