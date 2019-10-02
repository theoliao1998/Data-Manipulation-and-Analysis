import mrjob
from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"\b[\w']+\b") #regular expression

class TrigramCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    # +++your code here+++
    if len(words)>=3:
        for i in range(len(words)-2):
            yield (words[i]+" "+words[i+1]+" "+words[i+2]).lower(), 1

  def combiner(self, trigram, counts):
    # +++your code here+++
    yield trigram, sum(counts)
        
  def reducer(self, trigram, counts):
    # +++your code here+++
    yield trigram, repr(sum(counts))

if __name__ == '__main__':
  TrigramCount.run()
