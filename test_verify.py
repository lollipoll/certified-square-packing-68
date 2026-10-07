from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import unittest

from verify import (check_polygons, exact_check, numerical_check,
                    rational_polygons, sincos, atan, pi)


def packing(side, rows):
    return dict(schema='independent-square-certificate/v1',n=len(rows),
                container_side=str(side),
                squares=[dict(zip(('x','y','t'),map(str,row))) for row in rows])


class GeometryTests(unittest.TestCase):
    def test_one_square_all_walls_touch(self):
        r = exact_check(packing(1,[(0,0,0)]),1)
        self.assertTrue(r['valid'])
        self.assertEqual(r['minimum_wall_gap'],'0')

    def test_four_grid_squares_edges_and_corners_touch(self):
        q = packing(2,[(x,y,0) for x in (F(-1,2),F(1,2)) for y in (F(-1,2),F(1,2))])
        r = exact_check(q,4)
        self.assertTrue(r['valid'])
        self.assertEqual(r['pairs_checked'],6)
        self.assertEqual(r['minimum_pair_gap'],'0')

    def test_rational_rotation_wall_contact(self):
        # t=1/3 -> cos=4/5, sin=3/5 -> enclosing width 7/5.
        self.assertTrue(exact_check(packing(F(7,5),[(0,0,F(1,3))]),1)['valid'])

    def test_rotated_edge_contact(self):
        rows = [(F(-2,5),F(-3,10),F(1,3)),(F(2,5),F(3,10),F(1,3))]
        r = exact_check(packing(F(11,5),rows),2)
        self.assertTrue(r['valid'])
        self.assertEqual(r['minimum_pair_gap'],'0')

    def test_overlap(self):
        r = exact_check(packing(3,[(0,0,0),(F(9,10),0,0)]),2)
        self.assertFalse(r['valid'])
        self.assertEqual(F(r['max_pair_penetration']),F(1,10))

    def test_identical_squares_overlap(self):
        r = exact_check(packing(2,[(0,0,0),(0,0,0)]),2)
        self.assertFalse(r['valid'])
        self.assertEqual(F(r['max_pair_penetration']),1)

    def test_tiny_overlap_rejected_exact_and_numerical(self):
        q = packing(3,[(0,0,0),(1-F(1,10**30),0,0)])
        self.assertFalse(exact_check(q,2)['valid'])
        self.assertFalse(numerical_check(q,2)['valid'])
        self.assertTrue(numerical_check(q,2,tolerance='1e-12')['valid'])

    def test_tiny_boundary_violation(self):
        q = packing(1,[(F(1,10**30),0,0)])
        r = exact_check(q,1)
        self.assertFalse(r['valid'])
        self.assertEqual(F(r['max_boundary_violation']),F(1,10**30))
        self.assertFalse(numerical_check(q,1)['valid'])

    def test_rotated_boundary_violation(self):
        self.assertFalse(exact_check(packing(F(139,100),[(0,0,F(1,3))]),1)['valid'])

    def test_wrong_external_count(self):
        with self.assertRaises(ValueError):
            exact_check(packing(3,[(0,0,0)]),2)

    def test_false_declared_count(self):
        q = packing(3,[(0,0,0)])
        q['n']=2
        with self.assertRaises(ValueError):
            exact_check(q,2)

    def test_nonunit_polygon(self):
        q = rational_polygons([(F(0),F(0),F(0))])
        q[0] = [(x*(1+F(1,10**30)),y) for x,y in q[0]]
        r = check_polygons(q,F(3),1)
        self.assertFalse(r['valid'])
        self.assertGreater(F(r['unit_squared_error']),0)

    def test_rhombus_is_not_square(self):
        # Four unit sides alone are insufficient.
        q = [[(F(0),F(0)),(F(1),F(0)),(F(8,5),F(4,5)),(F(3,5),F(4,5))]]
        r = check_polygons(q,F(4),1)
        self.assertEqual(F(r['unit_squared_error']),0)
        self.assertFalse(r['valid'])
        self.assertEqual(F(r['right_angle_dot_error']),F(3,5))

    def test_rotation_invariance_and_reordering(self):
        q = packing(4,[(0,0,F(1,3)),(F(4,5),F(3,5),F(1,3))])
        first=exact_check(q,2)
        q['squares'].reverse()
        self.assertEqual(first['minimum_pair_gap'],exact_check(q,2)['minimum_pair_gap'])

    def test_separator_only_from_second_square(self):
        # Axis-aligned bounding boxes overlap in BOTH dimensions, but the
        # second square's tilted edge supplies a positive separating gap.
        q=packing(5,[(0,0,0),(F(7,10),F(11,10),F(1,3))])
        r=exact_check(q,2)
        self.assertTrue(r['valid'])
        self.assertEqual(F(r['minimum_pair_gap']),F(1,50))
        self.assertEqual(r['pair_witness']['axis_owner'],1)

    def test_decimal_trigonometry(self):
        with localcontext() as ctx:
            ctx.prec=100
            s,c=sincos(pi()/2)
            self.assertLess(abs(s-1),D('1e-95'))
            self.assertLess(abs(c),D('1e-95'))
            self.assertLess(abs(atan(D(1))-pi()/4),D('1e-95'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
