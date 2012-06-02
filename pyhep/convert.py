import LesHouchesEvents as LHE
from pyhep import *
from storage import EventCollection

def convert_from_LHE( infilename, outfilename) :
    """Import events from LHE files. Return a list of Events"""
    lhe = LHE.LHEventReader(infilename)
    ec = EventCollection(outfilename)
    for lhe_event in lhe.events() :
        particles = map(LHE_particle_to_pyhep, lhe_event.particles)
        event = Event(particles)
        event.metadata['comment'] = lhe_event.comment
        event.metadata['idprup'] = lhe_event.idprup()
        ec.add_event(event)

    ec.save()
    return ec

def LHE_particle_to_pyhep(p) :
    """Convert an LHE particle to a pyhep particle"""
    p4 = FourVector(p.px(), p.py(), p.pz(), p.energy())
    pdgID = p.idup()
    status = p.istup()

    p_out = Particle(p4, pdgID)
    p_out.status = status

    return p_out
