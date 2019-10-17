# usage:
# python casualty_uk.py ../datasets/uk/Casualties0515.csv

import mrjob
from mrjob.job import MRJob

severity = {'1':'Fatal','2':'Serious','3':'Slight'}

class SeverityCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    data = line.split(',')
    if data[7] in {'1','2','3'}:
        yield severity[data[7]], 1
        
  def reducer(self, severity, counts):
    yield severity, repr(sum(counts))

if __name__ == '__main__':
  SeverityCount.run()