import json
import math
import re

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_hw6")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

input_file = sc.textFile("hdfs:///var/umsi618/hw5/review.json")

inputs = input_file.map(lambda line: json.loads(line))

WORD_RE=re.compile(r"\b[\w]+\b")

def convert_dict_to_tuples(d):
    text = d['text']
    usefulness = d['useful']
    tokens = WORD_RE.findall(text)
    tuples = [(usefulness,t) for t in tokens]
    return tuples

usefulness_word = inputs.flatMap(convert_dict_to_tuples)

all_count = usefulness_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))

useful_word = usefulness_word.filter(lambda x: x[0]>5)
useful_count = useful_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))
                    

useless_word = usefulness_word.filter(lambda x: x[0]==0)
useless_count = useless_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))

all_review_count = all_count.map(lambda x: x[1]).sum()
useful_review_count = useful_count.map(lambda x: x[1]).sum()
useless_review_count = useless_count.map(lambda x: x[1]).sum()

freq_words = all_count.filter(lambda x: x[1]>1000).cache()
useful_t = freq_words.join(useful_count)
useless_t = freq_words.join(useless_count)

useful = useful_t.map(lambda x:(x[0], math.log(float(x[1][1])/useful_review_count) \
    - math.log(float(x[1][0])/all_review_count)))

sorted_useful = useful.sortBy(lambda x: x[1], ascending = False, numPartitions=1)

sorted_useful.saveAsTextFile('si618_hw6_theoliao_usefulreview.csv')

useless = useless_t.map(lambda x:(x[0], math.log(float(x[1][1])/useless_review_count) \
    - math.log(float(x[1][0])/all_review_count)))
sorted_useless = useless.sortBy(lambda x:x[1], ascending = False, numPartitions=1)

sorted_useless.saveAsTextFile('si618_hw6_theoliao_uselessreview.csv')
