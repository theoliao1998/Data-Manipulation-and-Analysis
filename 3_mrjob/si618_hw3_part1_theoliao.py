from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w]{5,}")


class MRMostUsedWord(MRJob):
    def mapper(self, _, line):
        # your code goes here
        words = WORD_RE.findall(line)
        for word in words:
            yield (word.lower(),1)
    
    def combiner(self, word, counts):
        # your code goes here
        yield (word,sum(counts))
    
    def reducer(self, word, counts):
        # your code goes here
        yield (word,sum(counts))



if __name__ == "__main__":
   MRMostUsedWord.run()

