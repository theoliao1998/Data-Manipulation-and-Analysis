#pyspark --master yarn --num-executors 35 --executor-memory 5g --executor-cores 4 --conf spark.ui.port="$(shuf -i 10000-60000 -n 1)"

import json
import math
import re

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_lec6")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

input_file = sc.textFile("hdfs:///var/umsi618/hw5/review.json")

inputs = input_file.map(lambda line: json.loads(line))

WORD_RE=re.compile(r"\b[\w]+\b")

def convert_dict_to_tuples(d):
    text = d['text']
    rating = d['stars']
    tokens = WORD_RE.findall(text.lower())
    tuples = [(rating,t) for t in tokens]
    return tuples

rating_word = inputs.flatMap(convert_dict_to_tuples)

all_count = rating_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))

pos_word = rating_word.filter(lambda x: x[0]>=5)
pos_count = pos_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))
                    
"""
[(u'halligan', 2), (u'kickasss', 2), (u'divinely', 95), (u'hasnbeen', 1), (u'oec', 1), 
(u'four', 36404), (u'prices', 179031), (u'conjuring', 15), (u'sentaron', 1), (u'otro', 155)]
"""

neg_word = rating_word.filter(lambda x: x[0]<=2)
neg_count = neg_word.map(lambda x: (x[1],1)) \
                    .reduceByKey(lambda x, y: (x + y))
"""
[(u'rasamalai', 4), (u'potillos', 1), (u'063016', 1), (u'varierty', 1), (u'four', 36260), 
(u'prices', 73835), (u'conjuring', 18), (u'sevens', 96), (u'profil', 1), (u'amminities', 1)]
"""

all_review_count = all_count.map(lambda x: x[1]).sum() #762235885
pos_review_count = pos_count.map(lambda x: x[1]).sum() #263994836
neg_review_count = neg_count.map(lambda x: x[1]).sum() #225489788

freq_words = all_count.filter(lambda x: x[1]>1000).cache()
step_3pos = freq_words.join(pos_count)
step_3neg = freq_words.join(neg_count)

positivity = step_3pos.map(lambda x:(x[0], math.log(float(x[1][1])/pos_review_count) \
    - math.log(float(x[1][0])/all_review_count)))

sorted_pos = positivity.sortBy(lambda x:x[1], ascending = False)
sorted_pos.saveAsTextFile('si618_hw6_theoliao_posreview.csv')

negativity = step_3neg.map(lambda x:(x[0], math.log(float(x[1][1])/neg_review_count) \
    - math.log(float(x[1][0])/all_review_count)))
sorted_neg = negativity.sortBy(lambda x:x[1], ascending = False)
sorted_neg.saveAsTextFile('si618_hw6_theoliao_negreview.csv')

