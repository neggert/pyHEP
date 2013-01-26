import pyhep
import sys
import matplotlib.pylab as plt
import itertools

mee = []

def good_electron(ele):
    return (ele.p4.pt > 20)

def pass_met(event):
    return (event.met().pt > 20)

evt_col = pyhep.EventCollection(sys.argv[1])
for e in itertools.ifilter(pass_met, evt_col.events()):
    electrons = filter(good_electron, e.electrons())
    if len(electrons) < 2:
        continue
    # sort by pt
    electrons.sort(key=lambda p: p.p4.pt, reverse=True)

    ee = electrons[0].p4+electrons[1].p4
    mee.append(ee.mass)
evt_col.close()

plt.hist(mee)
plt.show()
raw_input("...")

