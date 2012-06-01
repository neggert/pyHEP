#!/usr/bin/env python

# http://lcgapp.cern.ch/project/docs/lhef5.pdf

import math
import xml.etree.cElementTree as ET

def split_line(l):
    l = l.replace('\n','').replace('\t',' ')
    while '  ' in l:
        l = l.replace('  ', ' ')
    return [x for x in l.split(' ') if x]

class LHParticle:
    invalid = 1e99

    def __init__(self, raw_line):
        self.raw = split_line(raw_line)
        assert(len(self.raw) == 13)

    def idup(self):
        return int(self.raw[0])
    def istup(self):
        return int(self.raw[1])
    def mothup1(self):
        return int(self.raw[2])
    def mothup2(self):
        return int(self.raw[3])
    def icolup1(self):
        return int(self.raw[4])
    def icolup2(self):
        return int(self.raw[5])
    def pup1(self):
        return float(self.raw[6])
    def pup2(self):
        return float(self.raw[7])
    def pup3(self):
        return float(self.raw[8])
    def pup4(self):
        return float(self.raw[9])
    def pup5(self):
        return float(self.raw[10])
    def vtimup(self):
        return float(self.raw[11])
    def spinup(self):
        return float(self.raw[12])
    def id(self):
        return self.idup()
    def mothers(self):
        return self.mothup1(), self.mothup2()
    def px(self):
        return self.pup1()
    def py(self):
        return self.pup2()
    def pz(self):
        return self.pup3()
    def energy(self):
        return self.pup4()
    def mass(self):
        return self.pup5()
    def pt(self):
        return (self.px()**2 + self.py()**2)**0.5

#        self.theta = math.atan2(self.py, self.px)
#        den = self.e - self.pz
#        if abs(den) < 1e-5:
#            y = self.invalid
#        else:
#            rat = (self.e + self.pz)/(den)
#            if rat < 1e-99:
#                y = self.invalid
#            else:
#                y = 0.5*math.log(rat)
#        self.y = self.rapidity = y
#
#        ttho2 = math.tan(self.theta/2)
#        if ttho2 < 1e-99:
#            self.eta = self.invalid
#        else:
#            self.eta = -math.log(ttho2)

class LHEvent:
    def __init__(self, raw_header, raw_lines):
        self.particles = []
        self.parse_header(raw_header)
        self.parse_particle_lines(raw_lines)

    def parse_header(self, raw_header):
        self.raw = split_line(raw_header)
        assert(len(self.raw) == 6)

    def nup(self):
        return int(self.raw[0])
    def idprup(self):
        return int(self.raw[1])
    def xwgtup(self):
        return float(self.raw[2])
    def scalup(self):
        return float(self.raw[3])
    def aqedup(self):
        return float(self.raw[4])
    def aqcdup(self):
        return float(self.raw[5])

    def parse_particle_lines(self, raw_lines):
        for line in raw_lines:
            if not '#' in line :
                self.particles.append(LHParticle(line))
            else :
                self.comment = line
        assert(self.nup() == len(self.particles))


class LHEventReader:
    def __init__(self, filename, max_events=None):
        self.init = None
        self.events = []
        for event, elem in ET.iterparse(filename):
            if elem.tag == 'init':
                self.init = elem.text
            elif elem.tag == 'event':
                e = [x for x in elem.text.split('\n') if x]
                header = e[0]
                particle_lines = e[1:]
                lhe = LHEvent(header, particle_lines)
                self.events.append(lhe)
                if len(self.events) == max_events:
                    break

__all__ = [
    'LHParticle',
    'LHEvent',
    'LHEventReader'
    ]

if __name__ == '__main__':
    import sys
    lhe = LHEventReader(sys.argv[1])
