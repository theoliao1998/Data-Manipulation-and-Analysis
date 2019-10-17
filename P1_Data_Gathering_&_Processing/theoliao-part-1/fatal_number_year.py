import csv
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("si618_p1_fatal_number")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

## france
input_users = sc.textFile("france/users.csv")
input_accidents = sc.textFile("france/caracteristics.csv")

users_all_f = input_users.filter(lambda x: x[0]=='2') \
                            .map(lambda line: tuple([line.split(',')[i] for i in [0,3]]))
                    
users_fatal_f = users_all_f.filter(lambda x: x[1]=='2')

accidents_f = input_accidents.map(lambda line: tuple(line.split(',')[:2]))

fatal_france = users_fatal_f.join(accidents_f).map(lambda x: (int(x[1][1]),1)) \
                            .reduceByKey(lambda x,y: x+y) \
                            .sortBy(lambda x: x[0], ascending = False).cache()

fatal_france.saveAsTextFile("fatal_number_in_France")

## uk
input_uk = sc.textFile("uk/Casualties0515.csv")

users_all_uk = input_uk.filter(lambda x: x[0]=='2') \
                        .map(lambda line: tuple([line.split(',')[i] for i in [0,7]]))

users_fatal_uk = users_all_uk.filter(lambda x: x[1]=='1')

fatal_uk = users_fatal_uk.map(lambda x: (int(x[0][2:4]),1)) \
                            .reduceByKey(lambda x,y: x+y) \
                            .sortBy(lambda x: x[0], ascending = False).cache()

fatal_uk.saveAsTextFile("fatal_number_in_UK")

## overall fatal rate

users_all = users_all_uk.map(lambda x: (int(x[0][2:4]),1)) \
                            .reduceByKey(lambda x,y: x+y) \
                            .join(users_all_f.join(accidents_f).map(lambda x: (int(x[1][1]),1)) \
                            .reduceByKey(lambda x,y: x+y)) \
                            .map(lambda x: (x[0],x[1][0]+x[1][1])) \
                            .sortBy(lambda x: x[0], ascending = False)

fatal_all = fatal_uk.join(fatal_france) \
                        .map(lambda x: (x[0],x[1][0]+x[1][1]))

fatal_rate = fatal_all.join(users_all) \
                        .map(lambda x: (x[0],float(x[1][0])/x[1][1])).cache()

fatal_rate.saveAsTextFile("Overall_fatal_rate")

