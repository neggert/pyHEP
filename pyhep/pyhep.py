"""
A package for working with high-energy physics data in python.
Many of the ideas in this package are borrowed from ROOT (http://root.cern.ch),
but implemented in a more python-like way.
Author: Nic Eggert (nse23@cornell.edu)
"""

from math import sqrt, sin, cos, tan, atan2, acos, log, sinh

import persistent
import functools

class FourVector(persistent.Persistent) :
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

    def mass():
        doc = "Particle mass"
        def fget(self):
            return sqrt(self.energy**2-self.p**2)
        return locals()
    mass = property(**mass())

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

class Particle(persistent.Persistent):
    """
    Class representing a particle
    """
    def __init__(self, p4, **kwargs):
        """
        Initialize the Particle

        Arguments:
        p4 - the particle's 4-momentum
        **kwargs - used to set any of the particle's other properties

        options:
        pdgID - Particle Data Group ID
        charge - Electric charge of the particle
        """

        self.p4 = p4
        self._set_properties_from_dict(kwargs)

    def _set_properties_from_dict(self, prop_dict):
        for key in prop_dict.keys():
            setattr(self, key, prop_dict[key])

    def p4():
        doc = "The four-momentum of the particle"
        def fget(self):
            return self._p4
        def fset(self, value):
            self._p4 = value
        return locals()
    p4 = property(**p4())

    def pdgID():
        doc = "The Particle Data Group ID number"
        def fget(self):
            return self._pdgID
        def fset(self, value):
            self._pdgID = value
        return locals()
    pdgID = property(**pdgID())

    def charge():
        doc = "The particle's charge"
        def fget(self):
            return self._charge
        def fset(self, value):
            self._charge = value
        return locals()
    charge = property(**charge())


class Event(persistent.Persistent):
    """
    Class representing an event. For now this is just a list of particles and a dict for metadata
    """
    def __init__(self, *args) :
        """Initilialize empty or with a list of particles"""
        if len(args) == 0 :
            self.particles_ = []
        elif len(args) == 1 :
            self.particles_ = args[0]
        self.metadata = {}

    def metadata():
        doc = "The metadata property."
        def fget(self):
            return self._metadata
        def fset(self, value):
            self._metadata = value
        def fdel(self):
            del self._metadata
        return locals()
    metadata = property(**metadata())

    def particles(self, selection_func=None) :
        """
        Return particles in an event, optionally passed through a filter

        Arguments:
        selection_func - None, or a function that takes a single particle as an argument
        and returns a boolean indicating whether the particle should be included.
        """
        if selection_func == None:
            return self.particles_
        else:
            return filter(selection_func, self.particles_)

    def particles_with_pdgId(self, pdgId):
        particle_filter = functools.partial(_filter_by_pdgId, pdgId=pdgId)
        return self.particles(particle_filter)

    def electrons(self):
        return self.particles_with_pdgId(11)

    def muons(self):
        return self.particles_with_pdgId(13)

    def met(self, pdgIDs_to_ignore=[12, 14, 16]):
        """
        Return the missing transverse momentum 4-vector of
        the event. This is just the negative sum of all the
        particles that aren't in pdgIDs_to_ignore.

        Note that if you want to exclude particles with e.g. status=3,
        just make a sub-class.
        """
        return sum([p.p4 for p in self.particles() if p.pdgID not in pdgIDs_to_ignore],
                   FourVector())

    def add_particle(self, particle) :
        """
        Add a particle to the event. This can be of type Particle or any
        class that inherits from Particle
        """
        self.particles_.append(particle)

class GenEvent(Event):
    """Generator-level event"""
    def __init__(self, *args):
        super(GenEvent, self).__init__(*args)

    def add_particle(self, particle) :
        """
        Add a particle to the event. This can be of type GenParticle or any
        class that inherits from GenParticle
        """
        if not hasattr(particle, "status"):
            raise ValueError("Particles added to GenEvent must inherit from GenParticle")
        self.particles_.append(particle)

    def met(self, pdgIDs_to_ignore=[12, 14, 16]):
        """
        Return the missing transverse momentum 4-vector of
        the event. This is just the negative sum of all the
        particles that aren't in pdgIDs_to_ignore and have
        status = 1.
        """
        status_filter = functools.partial(_filter_by_status, status=1)
        return sum([p.p4 for p in self.particles(status_filter) if p.pdgID not in pdgIDs_to_ignore],
                   FourVector())

def _filter_by_pdgId(particle, pdgId):
    """Function for filtering particles py pdgID"""
    return abs(particle.pdgID) == pdgId

def _filter_by_status(particle, status):
    return particle.status == status





