import pyhep
import sys
import matplotlib.pylab as plt

mee = []

evt_col = pyhep.EventCollection(sys.argv[1])
for e in evt_col.events():
    electrons = e.particles_with_pdgId(11)
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

