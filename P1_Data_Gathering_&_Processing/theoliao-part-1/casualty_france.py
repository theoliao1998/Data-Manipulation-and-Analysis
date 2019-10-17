# usage:
# python casualty_france.py ../datasets/france/users.csv

import mrjob
from mrjob.job import MRJob
import re

class SeverityCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    data = line.split(',')
    if data[3] in {'1','4'}:
        yield "Slight", 1
    elif data[3]=='3':
        yield "Serious",1
    else:
        yield "Fatal",1
        
  def reducer(self, severity, counts):
    yield severity, repr(sum(counts))

if __name__ == '__main__':
  SeverityCount.run()