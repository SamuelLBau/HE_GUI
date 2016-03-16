import sys
import os

from log2CSV import log2CSV

irLog = os.path.join(os.path.dirname(__file__),"IRlog.txt")
visLog = os.path.join(os.path.dirname(__file__),"IRlog.txt")
irCSV = os.path.join(os.path.dirname(__file__),"IRParsed.csv")
visCSV = os.path.join(os.path.dirname(__file__),"visParsed.csv")

print("IR log: %s" %(irLog))

log2CSV(irLog,visLog,irCSV,visCSV)