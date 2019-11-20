from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_lab5")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)


#Q0

nfldf = sqlContext.read.json("hdfs:///var/umsi618/lecture5/NFLPlaybyPlay2015.json")
nfldf.registerTempTable("nfl")


#Q1
q1_1 = sqlContext.sql("select GameID, Posteam, sum(YardsGained) as totalYards from nfl where posteam is not NULL group by GameID, Posteam order by GameID")
q1_1.registerTempTable("teamYardsPerGame")
q1_2 = sqlContext.sql('select t1.Posteam as team1, t2.Posteam as team2, t1.totalYards as team1Yards, t2.totalYards as team2Yards, (t1.totalYards-t2.totalYards) as deltaYards from teamYardsPerGame as t1 join teamYardsPerGame as t2 where t1.GameID=t2.GameID and t1.Posteam!=t2.Posteam')
q1_2.registerTempTable("deltaYardsPerGame")
q1_3 = sqlContext.sql('select team1, mean(deltaYards) as meanDeltaYards from deltaYardsPerGame group by team1 order by meanDeltaYards desc')

res = q1_3.rdd.map(lambda x: x[0]+'\t'+repr(x[1]))
res.collect()
res.saveAsTextFile("si618_lab5_output_1")

#Q2
q2 = sqlContext.sql("""
WITH t AS 
(SELECT posteam, PlayType, count(*) AS count 
          FROM nfl 
          WHERE posteam IS NOT NULL AND PlayType IN ('Pass','Run') 
  	      GROUP BY posteam, PlayType)
SELECT A.posteam, (A.count / B.count) as ratio FROM t as A join t as B on A.posteam=B.posteam and A.PlayType='Run' and B.PlayType='Pass'
ORDER BY ratio
""")

res2 = q2.rdd.map(lambda x: x[0]+'\t'+repr(x[1]))
res2.collect()
res2.saveAsTextFile("si618_lab5_output_2")
