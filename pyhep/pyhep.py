"""
A package for working with high-energy physics data in python.
Many of the ideas in this package are borrowed from ROOT (http://root.cern.ch),
but implemented in a more python-like way.
Author: Nic Eggert (nse23@cornell.edu)
"""

from math import sqrt, sin, cos, tan, atan2, acos, log, sinh

import persistent
import functools


class FourMomentum(persistent.Persistent):
    """
    A four-vector class. Components in various representations are accessed
    using properties that act just like data members.

    For example, we can specify a four-vector in cartesian coordinates, then
    ask for its components in pt-eta-phi coordinates.

    >>> p4 = FourMomentum.from_x_y_z_m(50,60,70,10)
    >>> p4.eta
    0.8060830589013741
    >>> p4.theta
    0.8400523908062
    >>> p4.phi
    0.8760580505981934
    >>> p4.energy
    105.35653752852738

    You can set the components however you want and the underlying structure
    will change in a sensible way. For example, setting the phi component
    leaves the z direction alone, as well as the magnitude of the vector in
    the x-y plane, but changes x and y so that the vector has the requested
    value of phi. For components where the correct action would be ambiguous,
    the setter is not implemented.

    >>> p4.phi = -1.2
    >>> p4.px
    -72.79457969107862
    >>> p4.py
    28.301045344637032

    You can also perform arithemetic with FourMomenta as you might expect
    >>> p4b = FourMomentum.from_x_y_z_m(30,20,10,40)
    >>> (p4+p4b).pt
    96.48246647112506
    >>> (p4*3).pt
    327.6246013042608

    Note that under the hood, this class keeps track of the x,y,z, and s
    components, where s is the measure or invariant mass, and is immutable.
    Everything else is calculated on the fly.
    """
    def __init__(self):
        """Initialize using cartesian coordinates or nothing"""
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.m = 0.

    @classmethod
    def from_x_y_z_m(cls, x, y, z, m):
        """
        Initialize from three-momentum components and the mass

        Example:
        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> round(p4.energy, 6)
        40.926764
        """
        p4 = cls()
        p4.x = x
        p4.y = y
        p4.z = z
        p4.m = m
        return p4

    @classmethod
    def from_x_y_z_e(cls, x, y, z, e):
        """
        Initialize from three-momentum components and the energy

        Example:
        >>> p4 = FourMomentum.from_x_y_z_e(5,5,5,40)
        >>> round(p4.mass, 6)
        39.051248
        """
        m = sqrt(e**2-x**2-y**2-z**2)
        return cls.from_x_y_z_m(x, y, z, m)

    @classmethod
    def from_pt_theta_phi_m(cls, pt, theta, phi, m):
        """
        Initialize from transvsere momentum, angles, and the mass

        Example:
        >>> p4 = FourMomentum.from_pt_theta_phi_m(30,1,3,40)
        >>> round(p4.energy, 6)
        61.711823
        """
        x = pt*sin(phi)
        y = pt*sin(phi)
        z = pt*tan(theta)
        m = m
        return cls.from_x_y_z_m(x, y, z, m)

    @classmethod
    def from_pt_theta_phi_e(cls, pt, theta, phi, e):
        """
        Initialize from transvsere momentum, angles, and the energy

        Example:
        >>> p4 = FourMomentum.from_pt_theta_phi_e(30,1,3,60)
        >>> round(p4.mass, 6)
        37.164315
        """
        x = pt*sin(phi)
        y = pt*sin(phi)
        z = pt*tan(theta)
        return cls.from_x_y_z_e(x, y, z, e)

    @property
    def px(self):
        """The x component of the momentum."""
        return self.x

    @px.setter
    def px(self, value):
            self.x = value

    @property
    def py(self):
        """The y component of the momentum"""
        return self.y
    
    @py.setter
    def py(self, value):
        self.y = value

    @property
    def pz(self):
        """The z component of the momentum"""
        return self.z
    
    @pz.setter
    def pz(self, value):
        self.z = value

    @property
    def mass(self):
        """The invariant mass. Immutatable"""
        return self.m
    
    @mass.setter
    def mass(self, value):
        raise NotImplementedError("Cannot change the invariant mass of a FourMomentum")

    @property
    def p(self):
        """
        The magnitude of the three-momentum. This is just sqrt(px^2+py^2+pz^2). Setting the
        momentum fixes the angles and mass, but changes the momentum vector and energy.
        For example:

        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> round(p4.p, 6)
        8.660254
        >>> p4.p = 30
        >>> round(p4.theta, 6)
        0.955317
        >>> round(p4.phi, 6)
        0.785398
        >>> round(p4.energy, 6)
        50.0
        >>> round(p4.pt, 6)
        24.494897
        """
        return sqrt(self.x**2+self.y**2+self.z**2)
    
    @p.setter
    def p(self, value):
        """Set the magnitude of the three-momentum"""
        theta = self.theta
        self.pt = value*abs(sin(theta))
        self.pz = value*cos(theta)

    @property
    def energy(self):
        """The energy of the four-vector."""
        return sqrt(self.m**2+self.p**2)

    @energy.setter
    def energy(self, value):
        """
        Set the energy of the four-vector. Leave the mass and angles fixed, change the magnitude of the 3-vector

        Example:
        >>> p4 = FourMomentum(50,60,70,10)
        >>> round(p4.energy, 6)
        105.35653752852738
        >>> p4.energy = 150
        >>> round(p4.p, 6)
        149.66629547095766
        """
        if value < 0:
            raise ValueError("energy must be greater than or equal to 0.")
        new_p = sqrt(value**2-self.mass**2)
        # scale all of the momentum components to give the correct total momentum
        scale = new_p/self.p
        self.px *= scale
        self.py *= scale
        self.pz *= scale


    @property
    def pt(self):
        """
        The transverse momentum. That is, the momentum in the x-y plane.
        Calculated by sqrt(px**2+py**2).

        When the transverse momentum is set, keep the polar and azimuthal
        angles fixed, as well as the mass.

        Example:
        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> round(p4.pt, 6)
        7.071068
        >>> p4.pt = 30
        >>> round(p4.px, 6)
        21.213203
        >>> round(p4.py, 6)
        21.213203
        >>> round(p4.pz, 6)
        5.0
        >>> round(p4.energy, 6)
        50.249378
        >>> round(p4.phi, 6)
        0.785398
        """
        return sqrt(self.x**2+self.y**2)
    
    @pt.setter
    def pt(self, value):
        """
        Set the transverse momentum, keeping the polar and azimuthal angles fixed, as well as the mass.
        """
        if value < 0:
            raise ValueError("pt must be greater than or equal to 0.")
        phi = self.phi
        self.px = value*sin(phi)
        self.py = value*cos(phi)
        self.energy = sqrt(self.p**2+self.mass**2)

    @property
    def phi(self):
        """
        The azimuthal angle in the x-y plane. When phi is set, keep the z component and
        transverse momentum unchanged. Only change the x and y components to give the
        correct angle.

        Example:
        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> p4.phi = -1.2
        >>> round(p4.px, 6)
        -6.590512
        >>> round(p4.py, 6)
        2.562256
        >>> round(p4.pz, 6)
        5.0
        >>> p4.mass
        40
        """
        return atan2(self.py, self.px)
    
    @phi.setter
    def phi(self, value):
        """Set the value of phi"""
        pt = self.pt
        self.x = pt*sin(value)
        self.y = pt*cos(value)

    @property
    def theta(self):
        """
        The polar angle of the vector. When setting theta, preserve total energy and momentum,
        as well as the azimuthal angle.

        Example:
        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> round(p4.theta, 6)
        0.955317
        >>> p4.theta = -3.0
        >>> round(p4.pz, 6)
        -8.573587
        >>> round(p4.phi, 6)
        0.785398
        """
        return acos(self.z/self.p)
    
    @theta.setter
    def theta(self, value):
        """Set the polar angle"""
        p = self.p
        self.pt = p*abs(sin(value))
        self.pz = p*cos(value)

    @property
    def eta(self):
        """
        The pseudo-rapidity.

        Example:
        >>> p4 = FourMomentum.from_x_y_z_m(5,5,5,40)
        >>> p4.eta
        0.6584789484624084
        """
        return -log(tan(self.theta/2))
    
    @eta.setter
    def eta(self, value):
        raise NotImplementedError("Eta cannot be set")

    def __add__(self, other) :
        """Add with another FourMomentum"""
        return FourMomentum(self.x+other.x, self.y+other.y, self.z+other.z, self.t+other.t)

    def __iadd__(self, other) :
        """In place add to another FourMomentum"""
        self = self + other

    def __neg__(self, other) :
        """Negative of all components"""
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        self.t = -self.t

    def __sub__(self, other) :
        """Subtract another FourMomentum"""
        return self + -other

    def __isub__(self, other) :
        """In-place subtract another FourMomentum"""
        self = self - other

    def __mul__(self, scalar) :
        """Multiply all components by a scalar"""
        return FourMomentum(self.x*scalar, self.y*scalar, self.z*scalar, self.t*scalar)

    def __imul__(self, scalar) :
        """Multiply all components by a scalar in place"""
        self = self*scalar

    def dot(self, other) :
        """Scalar product with another FourMomentum"""
        return self.t*other.t-self.x*other.x-self.y*other.y-self.z*other.z

    def __eq__(self, other) :
        """Compare to another FourMomentum"""
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
                   FourMomentum())

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
                   FourMomentum())

def _filter_by_pdgId(particle, pdgId):
    """Function for filtering particles py pdgID"""
    return abs(particle.pdgID) == pdgId

def _filter_by_status(particle, status):
    return particle.status == status

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()



