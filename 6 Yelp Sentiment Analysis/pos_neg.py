#pyspark --master yarn --num-executors 35 --executor-memory 5g --executor-cores 4 --conf spark.ui.port="$(shuf -i 10000-60000 -n 1)"

import json
import math
import re

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_hw5")
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

negativity = step_3neg.map(lambda x:(x[0], math.log(float(x[1][1])/neg_review_count) \
    - math.log(float(x[1][0])/all_review_count)))
sorted_neg = negativity.sortBy(lambda x:x[1], ascending = False)







t1 = sqlContext.sql("""
WITH m AS
(SELECT user_id, business_id FROM review WHERE stars>1)
SELECT count(*) as cnt FROM
(SELECT a.user_id, b.city FROM m AS a JOIN business AS b WHERE a.business_id=b.business_id GROUP BY a.user_id, b.city)
GROUP BY user_id
""")
t1.registerTempTable("t1")


max_city_num = sqlContext.sql("SELECT MAX(cnt) as max FROM t1").rdd.map(lambda x: x.max).collect()[0]

hist = t1.rdd.map(lambda x: x.cnt).histogram(list(range(1,max_city_num+2)))

data = list(zip(hist[0][:-1],hist[1]))
df = sqlContext.createDataFrame(data, ["cities", "yelp users"])


df.coalesce(1).write.format('com.databricks.spark.csv').save('si618_hw5_theoliao.csv',header = 'true')

##### for good reviews #####
t2 = sqlContext.sql("""
WITH m AS
(SELECT user_id, business_id FROM review WHERE stars>3)
SELECT count(*) as cnt FROM
(SELECT a.user_id, b.city FROM m AS a LEFT JOIN business AS b WHERE a.business_id=b.business_id GROUP BY a.user_id, b.city)
GROUP BY user_id
""")
t2.registerTempTable("t2")


max_city_num2 = sqlContext.sql("SELECT MAX(cnt) as max FROM t2").rdd.map(lambda x: x.max).collect()[0]

hist2 = t2.rdd.map(lambda x: x.cnt).histogram(list(range(1,max_city_num2+2)))

data2 = list(zip(hist2[0][:-1],hist2[1]))
df2 = sqlContext.createDataFrame(data2, ["cities", "yelp users"])


df2.coalesce(1).write.format('com.databricks.spark.csv').save('si618_hw5_theoliao_goodreview.csv',header = 'true')


##### for bad reviews #####
t3 = sqlContext.sql("""
WITH m AS
(SELECT user_id, business_id FROM review WHERE stars<3)
SELECT count(*) as cnt FROM
(SELECT a.user_id, b.city FROM m AS a LEFT JOIN business AS b WHERE a.business_id=b.business_id GROUP BY a.user_id, b.city)
GROUP BY user_id
""")
t3.registerTempTable("t3")


max_city_num3 = sqlContext.sql("SELECT MAX(cnt) as max FROM t3").rdd.map(lambda x: x.max).collect()[0]

hist3 = t3.rdd.map(lambda x: x.cnt).histogram(list(range(1,max_city_num3+2)))

data3 = list(zip(hist3[0][:-1],hist3[1]))
df3 = sqlContext.createDataFrame(data3, ["cities", "yelp users"])


df3.coalesce(1).write.format('com.databricks.spark.csv').save('si618_hw5_theoliao_badreview.csv',header = 'true')
