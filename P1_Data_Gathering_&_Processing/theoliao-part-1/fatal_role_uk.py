# usage:
# python fatal_role_uk.py uk/Casualties0515.csv

import mrjob
from mrjob.job import MRJob
import re

user_catagory = {'1':'Driver','2':'Passenger','3':'Pedestrian'}

class FatalCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    data = line.split(',')
    if data[7] == '1': # Casualty_Severity is fatal
        yield user_catagory[data[3]], 1
        
  def reducer(self, cata, counts):
    yield cata, repr(sum(counts))

if __name__ == '__main__':
  FatalCount.run()