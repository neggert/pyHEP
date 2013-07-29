import unittest

from pyhep import *


class TestFourMomentum(unittest.TestCase):
    """Tests for FourMomentum class"""

    def almost_equal(self, p1, p2):
        self.assertAlmostEqual(p1.px, p2.px)
        self.assertAlmostEqual(p1.py, p2.py)
        self.assertAlmostEqual(p1.pz, p2.pz)
        self.assertAlmostEqual(p1.energy, p2.energy)

    def setUp(self):
        self.p1 = FourMomentum.from_x_y_z_m(10, 20, 30, 40)
        self.p2 = FourMomentum.from_x_y_z_m(20, 30, 40, 50)

    def test_from_x_y_z_m(self):
        p = FourMomentum.from_x_y_z_m(10, 20, 30, 40)
        self.assertEqual(p, self.p1)

    def test_from_x_y_z_e(self):
        p = FourMomentum.from_x_y_z_e(10, 20, 30, 54.772255751)
        self.almost_equal(p, self.p1)

    def test_from_pt_theta_phi_m(self):
        p = FourMomentum.from_pt_theta_phi_m(50, 0.5, 1.0, 10)
        p2 = FourMomentum.from_x_y_z_m(p.px, p.py, p.pz, p.mass)
        self.almost_equal(p, p2)

    def test_from_pt_theta_phi_e(self):
        p = FourMomentum.from_pt_theta_phi_e(50, 0.5, 1.0, 80)
        p2 = FourMomentum.from_x_y_z_m(p.px, p.py, p.pz, p.mass)
        self.almost_equal(p, p2)

    def test_from_pt_eta_phi_m(self):
        p = FourMomentum.from_pt_eta_phi_m(50, 0.1, 1.0, 10)
        p2 = FourMomentum.from_x_y_z_m(p.px, p.py, p.pz, p.mass)
        self.almost_equal(p, p2)

    def test_from_pt_eta_phi_e(self):
        p = FourMomentum.from_pt_eta_phi_e(50, 0.1, 1.0, 300)
        p2 = FourMomentum.from_x_y_z_m(p.px, p.py, p.pz, p.mass)
        self.almost_equal(p, p2)
