import persistent
from fourmomentum import FourMomentum
import functools


class Event(persistent.Persistent):
    """
    Class representing an event. Just a list of particles and a dict for metadata.
    Intended to be a base class.
    """
    def __init__(self, particles=None, metadata=None):
        """Initilialize empty or with a list of particles"""
        if particles is None:
            self.particles_ = []
        else:
            self.particles_ = particles
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata

    def particles(self, selection_func=None):
        """
        Return particles in an event, optionally passed through a filter

        Arguments:
        selection_func - None, or a function that takes a single particle as an argument
        and returns a boolean indicating whether the particle should be included.
        """
        if selection_func is None:
            return self.particles_
        else:
            return filter(selection_func, self.particles_)

    def particles_with_pdgID(self, pdgId):
        """
        Return an list of only particles with the abs(pdgID) equal to the
        one given.

        Example:
        >>> from particles import Particle, Electron
        >>> ele = Electron(FourMomentum.from_x_y_z_m(10,20,30,0.000511), 1)
        >>> nu = Particle(FourMomentum.from_x_y_z_m(-10,-20,-30,0), 12, 0)
        >>> e = Event([ele, nu])
        >>> len(e.particles_with_pdgID(12))
        1
        >>> e.particles_with_pdgID(12)[0].pdgID
        12
        """
        particle_filter = functools.partial(_filter_by_pdgId, pdgId=pdgId)
        return self.particles(particle_filter)

    def electrons(self):
        """
        Convience method to return only electrons
        """
        return self.particles_with_pdgId(11)

    def muons(self):
        """
        Convenience method to return only muons
        """
        return self.particles_with_pdgId(13)

    def met(self, pdgIDs_to_ignore=[12, 14, 16]):
        """
        Return the missing transverse momentum 4-vector of
        the event. This is just the negative sum of all the
        particles that aren't in pdgIDs_to_ignore.

        Note that if you want to exclude particles with e.g. status=3,
        just make a sub-class.

        Example:
        >>> from particles import Particle, Electron
        >>> ele = Electron(FourMomentum.from_x_y_z_m(10,20,30,0.000511), 1)
        >>> nu = Particle(FourMomentum.from_x_y_z_m(-10,-20,-30,0), 12, 0)
        >>> e = Event([ele, nu])
        >>> round(e.met().pt, 6)
        22.36068
        """
        return sum([p.p4 for p in self.particles() if p.pdgID not in pdgIDs_to_ignore],
                   FourMomentum())

    def add_particle(self, particle):
        """
        Add a particle to the event. This can be of type Particle or any
        class that inherits from Particle
        """
        self.particles_.append(particle)


class GenEvent(Event):
    """
    Generator-level event. Adds convenience functions to filter particles
    by generator status.
    """
    def __init__(self, *args):
        super(GenEvent, self).__init__(*args)

    def add_particle(self, particle):
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

        Example:
        >>> from particles import GenParticle
        >>> ele = GenParticle(FourMomentum.from_x_y_z_m(10,20,30,0.000511), 1, 11, 1)
        >>> nu = GenParticle(FourMomentum.from_x_y_z_m(-10,-20,-30,0), 12, 0, 1)
        >>> nu2 = GenParticle(FourMomentum.from_x_y_z_m(-10,-20,-30,0), 12, 0, 3)
        >>> e = GenEvent([ele, nu, nu2])
        >>> round(e.met().pt, 6)
        22.36068
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
