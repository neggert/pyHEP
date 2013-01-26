import pyhep

class Lepton(pyhep.Particle):
    """Lepton particle"""
    def __init__(self, p4, **kwargs):
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

        super(Lepton, self).__init__(p4, **kwargs)

    def isolation():
        doc = "The isolation property."
        def fget(self):
            try :
                return self._isolation
            except AttributeError :
                raise UnboundLocalError('isolation must be set before it can be used')
        def fset(self, value):
            self._isolation = value
        return locals()
    isolation = property(**isolation())

class Electron(Lepton):
    """Electron particle"""
    def __init__(self, p4, **kwargs):
        super(Electron, self).__init__(p4, **kwargs)
        self.pdgID = 11

class Muon(Lepton):
    """Muon particle"""
    def __init__(self, p4, **kwargs):
        super(Muon, self).__init__(p4, **kwargs)
        self.pdgID = 13

class GenParticle(pyhep.Particle):
    """Particle from an event generator. Holds status information"""
    def __init__(self, p4, **kwargs):
        """
        Initialize the Particle

        Arguments:
        p4 - the particle's 4-momentum
        **kwargs - used to set any of the particle's other properties

        options:
        charge - Electric charge of the particle
        pdgId - Particle Data Group ID
        status - Generator status code
        """
        super(GenParticle, self).__init__(p4, **kwargs)

    def status():
        doc = "The status property."
        def fget(self):
            return self._status
        def fset(self, value):
            self._status = value
        def fdel(self):
            del self._status
        return locals()
    status = property(**status())

