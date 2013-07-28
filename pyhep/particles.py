import persistent
from fourmomentum import FourMomentum


class Particle(persistent.Persistent):
    """
    Class representing a particle. This is a fairly thin
    wrapper over the FourMomentum class, as the rest of the
    data associated with a particle is fairly trivial.

    This is mostly intended as a base class to be inherited by
    more specific implementations of different particles.

    Example:
    >>> muon = Particle(FourMomentum.from_x_y_z_e(10,20,30,40), 13, -1)
    >>> muon.p4.px
    10
    >>> muon.charge
    -1
    """
    def __init__(self, p4, pdgID, charge):
        """
        Initialize the Particle

        Arguments:
        p4 - the particle's 4-momentum
        pdgID - Particle Data Group ID. The sign is ignored by pyHEP functions
        charge - Electric charge of the particle (electron has -1)
        """

        self.p4 = p4
        self.pdgID = pdgID
        self.charge = charge


class Lepton(Particle):
    """
    Lepton particle. Inherits from particle, adding a check on the charge
    (must be +/-1) and an isolation variable. The isolation is optional
    and must be set after construction.

    Example:
    >>> l = Lepton(FourMomentum.from_x_y_z_m(10,20,30,0.000511), 11, 1)
    >>> l.isolation = 0.3
    >>> l.isolation
    0.3
    """
    def __init__(self, p4, pdgID, charge):
        """
        Initialize the Particle

        Arguments:
        p4 - the particle's 4-momentum
        **kwargs - used to set any of the particle's other properties

        options:
        charge - Electric charge of the particle
        pdgId - Particle Data Group ID
        isolation - isolation variable for the particle
        """
        if charge not in [-1, 1]:
            raise ValueError("Lepton charge must be +/-1")

        super(Lepton, self).__init__(p4, pdgID, charge)
        self.isolation = 0.


class Electron(Lepton):
    """Electron particle. Lepton with pdgID automatically set to 11"""
    def __init__(self, p4, charge):
        """
        Initialize the electron from a FourMomentum and a charge

        Example:
        >>> e = Electron(FourMomentum.from_x_y_z_m(10,20,30,0.000511), 1)
        >>> e.pdgID
        11
        """
        super(Electron, self).__init__(p4, 11, charge)


class Muon(Lepton):
    """Muon. Lepton with pdgID automatically set to 13"""
    def __init__(self, p4, charge):
        """
        Initialize the muon from a FourMomentum and a charge

        Example:
        >>> m = Muon(FourMomentum.from_x_y_z_m(10,20,30,0.106), 1)
        >>> m.pdgID
        13
        """
        super(Muon, self).__init__(p4, 13, charge)


class GenParticle(Particle):
    """
    Particle from an event generator. Inherits from Particle and adds an
    extra member to hold the generator status.

    Example:
    >>> muon = GenParticle(FourMomentum.from_x_y_z_e(10,20,30,40), 13, -1, 3)
    >>> muon.p4.px
    10
    >>> muon.charge
    -1
    >>> muon.status
    3
    """
    def __init__(self, p4, pdgID, charge, status):
        """
        Initialize the Particle

        Arguments:
        p4 - the particle's 4-momentum
        pdgID - Particle Data Group ID. The sign is ignored by pyHEP functions
        charge - Electric charge of the particle (electron has -1)
        status - The Generator status of the particle.
        """

        super(GenParticle, self).__init__(p4, pdgID, charge)
        self.status = status


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()

