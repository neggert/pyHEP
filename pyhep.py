"""
A package for working with high-energy physics data in python.
Many of the ideas in this package are borrowed from ROOT (http://root.cern.ch),
but implemented in a more python-like way.
Author: Nic Eggert (nse23@cornell.edu)
"""

from math import sqrt, sin, cos, tan, atan2, acos, log, sinh

class FourVector(object) :
    """A four-vector class"""
    def __init__ (self, *args) :
        """Initialize using cartesian coordinates or nothing"""
        if len(args) == 4 :
            self.x, self.y, self.z, self.t = args
        else :
            self.x = 0.
            self.y = 0.
            self.z = 0.
            self.t = 0.

    def px():
        doc = "The px property."
        def fget(self):
            return self.x
        def fset(self, value):
            self.x = value
        return locals()
    px = property(**px())

    def py():
        doc = "The py property."
        def fget(self):
            return self.y
        def fset(self, value):
            self.y = value
        return locals()
    py = property(**py())

    def pz():
        doc = "The pz property."
        def fget(self):
            return self.z
        def fset(self, value):
            self.z = value
        return locals()
    pz = property(**pz())

    def energy():
        doc = "The energy property."
        def fget(self):
            return self.t
        def fset(self, value):
            self.t = value
        return locals()
    energy = property(**energy())

    def p():
        doc = "Particle 3-momentum magnitude"
        def fget(self):
            return self.l
        return locals()
    p = property(**p())

    def m():
        doc = "Particle mass"
        def fget(self):
            return sqrt(self.energy**2-self.p**2)
        return locals()
    m = property(**m())

    def l():
        doc = "Length of 3-vector"
        def fget(self):
            return sqrt(self.x**2+self.y**2+self.z**2)
        return locals()
    l = property(**l())

    def pt():
        doc = "Transverse momentum"
        def fget(self):
            return sqrt(self.px**2+self.py**2)
        def fset(self, value):
            # preserve polar and azimuthal angle
            self.px = value*sin(self.phi)
            self.py = value*cos(self.phi)
            self.energy = self.p**2+self.m**2
        return locals()
    pt = property(**pt())

    def phi():
        doc = "The azimuthal angle"
        def fget(self):
            return atan2(self.y, self.x)
        def fset(self, value):
            self.x = self.l*sin(value)
            self.y = self.l*cos(value)
        return locals()
    phi = property(**phi())

    def theta():
        doc = "The polar angle"
        def fget(self):
            return acos(self.z/self.l)
        def fset(self, value):
            # preserve total momentum
            self.pt = self.l*sin(value)
            self.z = self.l*cos(value)
        return locals()
    theta = property(**theta())

    def eta():
        doc = "Pseudo-rapidity"
        def fget(self):
            return -log(tan(self.theta/2))
        def fset(self, value):
            # preserve pt
            self.pz = self.pt*sinh(value)
        return locals()
    eta = property(**eta())

    def __add__(self, other) :
        """Add with another FourVector"""
        return FourVector(self.x+other.x, self.y+other.y, self.z+other.z, self.t+other.t)

    def __iadd__(self, other) :
        """In place add to another FourVector"""
        self = self + other

    def __neg__(self, other) :
        """Negative of all components"""
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        self.t = -self.t

    def __sub__(self, other) :
        """Subtract another FourVector"""
        return self + -other

    def __isub__(self, other) :
        """In-place subtract another FourVector"""
        self = self - other

    def __mul__(self, scalar) :
        """Multiply all components by a scalar"""
        return FourVector(self.x*scalar, self.y*scalar, self.z*scalar, self.t*scalar)

    def __imul__(self, scalar) :
        """Multiply all components by a scalar in place"""
        self = self*scalar

    def dot(self, other) :
        """Scalar product with another FourVector"""
        return self.t*other.t-self.x*other.x-self.y*other.y-self.z*other.z

    def __eq__(self, other) :
        """Compare to another FourVector"""
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z) and (self.t == other.t)