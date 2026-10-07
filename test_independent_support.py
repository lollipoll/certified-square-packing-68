from fractions import Fraction as F
import unittest

from independent_support_check import inspect


def certificate(side, rows):
    return {
        'schema': 'independent-square-certificate/v1',
        'n': len(rows),
        'container_side': str(side),
        'squares': [dict(zip(('x', 'y', 't'), map(str, row))) for row in rows],
    }


class SupportChecks(unittest.TestCase):
    def test_wall_contact(self):
        result = inspect(certificate(1, [(0, 0, 0)]), 1)
        self.assertTrue(result['valid'])
        self.assertEqual(result['minimum_wall_gap'], '0')

    def test_rational_rotation(self):
        self.assertTrue(inspect(certificate(F(7, 5), [(0, 0, F(1, 3))]), 1)['valid'])

    def test_edge_contact(self):
        result = inspect(certificate(4, [(0, 0, 0), (1, 0, 0)]), 2)
        self.assertTrue(result['valid'])
        self.assertEqual(result['minimum_pair_gap'], '0')

    def test_tiny_overlap(self):
        self.assertFalse(inspect(certificate(4, [(0, 0, 0), (1 - F(1, 10**30), 0, 0)]), 2)['valid'])

    def test_tiny_wall_protrusion(self):
        self.assertFalse(inspect(certificate(1, [(F(1, 10**30), 0, 0)]), 1)['valid'])

    def test_wrong_external_count(self):
        with self.assertRaises(ValueError):
            inspect(certificate(1, [(0, 0, 0)]), 2)

    def test_identical_squares(self):
        self.assertFalse(inspect(certificate(4, [(0, 0, 0), (0, 0, 0)]), 2)['valid'])

    def test_second_square_axis(self):
        result = inspect(certificate(5, [(0, 0, 0), (F(7, 10), F(11, 10), F(1, 3))]), 2)
        self.assertTrue(result['valid'])
        self.assertEqual(F(result['minimum_pair_gap']), F(1, 50))

    def test_grid(self):
        rows = [(x, y, 0) for x in (F(-1, 2), F(1, 2)) for y in (F(-1, 2), F(1, 2))]
        result = inspect(certificate(2, rows), 4)
        self.assertTrue(result['valid'])
        self.assertEqual(result['pairs_checked'], 6)


if __name__ == '__main__':
    unittest.main(verbosity=2)
