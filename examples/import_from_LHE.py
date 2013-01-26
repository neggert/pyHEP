import sys
import pyhep.convert

outfile = sys.argv[1].split('.')[0]+".pyhep"
pyhep.convert.convert_from_LHE(sys.argv[1], outfile)
