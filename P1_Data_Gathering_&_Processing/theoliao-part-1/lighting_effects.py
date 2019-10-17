from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_p1_lighting")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
from pyspark.sql import functions as F


## france
users_f_df = spark.read.format("csv").option("header", "true").load("users.csv")

users_f_df = users_f_df.withColumn('grav',
    F.when(users_f_df['grav']==1,4).otherwise(users_f_df['grav'])) # update to combine slight injury and unscathed

accicents_f_df = spark.read.format("csv").option("header", "true").load("caracteristics.csv")

users_f_df.registerTempTable("users_f")
accicents_f_df.registerTempTable("accicents_f")

res_f = sqlContext.sql("""
WITH u AS
(SELECT Num_Acc, min(grav) AS grav FROM users_f GROUP BY Num_Acc)
SELECT a.lum, u.grav, COUNT(*) AS cnt FROM accicents_f AS a JOIN u ON a.Num_Acc = u.Num_Acc
GROUP BY a.lum, u.grav""")
res_f.registerTempTable("res_f")

## uk
uk_df = spark.read.format("csv").option("header", "true").load("Accidents0515.csv")
uk_df.registerTempTable("uk")

res_uk = sqlContext.sql("""
SELECT Light_Conditions, Accident_Severity, COUNT(*) AS cnt FROM uk GROUP BY Light_Conditions, Accident_Severity
""")
res_uk.registerTempTable("res_uk")

## combine
res =  sqlContext.sql("""
SELECT uk.Light_Conditions, uk.Accident_Severity, (f.cnt+uk.cnt) as cnt FROM res_f AS f, res_uk AS uk
WHERE
((f.lum=1 AND uk.Light_Conditions=1) OR (f.lum=3 AND uk.Light_Conditions=6) 
OR (f.lum=4 AND uk.Light_Conditions=5) OR (f.lum=5 AND uk.Light_Conditions=4)
) AND (f.grav = (uk.Accident_Severity+1)) ORDER BY uk.Light_Conditions, uk.Accident_Severity
""")

res.coalesce(1).write.format('com.databricks.spark.csv').save('lighting_effects_output',header = 'true')