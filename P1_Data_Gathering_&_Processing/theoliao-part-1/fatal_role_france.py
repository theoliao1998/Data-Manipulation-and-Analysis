# usage:
# python fatal_role_france.py france/users.csv

import mrjob
from mrjob.job import MRJob
import re

user_catagory = {'1':'Driver','2':'Passenger','3':'Pedestrian','4':'Pedestrian'}

class FatalCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    data = line.split(',')
    if data[3] == '2':
        yield user_catagory[data[2]], 1
        
  def reducer(self, cata, counts):
    yield cata, repr(sum(counts))

if __name__ == '__main__':
  FatalCount.run()