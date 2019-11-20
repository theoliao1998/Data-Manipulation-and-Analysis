from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_hw5")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

review_df = sqlContext.read.json("hdfs:///var/umsi618/hw5/review.json")
business_df = sqlContext.read.json("hdfs:///var/umsi618/hw5/business.json")
review_df.registerTempTable("review")
business_df.registerTempTable("business")

##### primary output #####
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
