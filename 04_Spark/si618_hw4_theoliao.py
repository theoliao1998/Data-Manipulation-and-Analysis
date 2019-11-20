import json
from pyspark import SparkContext
sc = SparkContext(appName="PySparksi618f19hw4")

input_file = sc.textFile("hdfs:///var/umsi618/hw4/business.json")

def cat(data):
    cat_list = []
    star = data.get('stars', None)
    highstar = 1 if (not(star is None) and star>=4.0) else 0
    city = data.get('city', None)
    r_c = data.get('review_count', None)
    categories_raw = data.get('categories', None)
    if not categories_raw:
        categories_raw = "Unknown"
    categories = categories_raw.split(', ')
    for c in categories:
        if r_c != None:
            cat_list.append(((city, c), (1, r_c, highstar)))
    return cat_list

res = input_file.map(lambda line: json.loads(line)) \
                .flatMap(cat) \
                .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2])) \
                .sortBy(lambda x: (x[0][0],-x[1][0]), ascending = True, numPartitions=1) \
                .map(lambda x: str(x[0][0])+"\t"+str(x[0][1])+"\t"+repr(x[1][0])+"\t"+repr(x[1][1])+"\t"+repr(x[1][2]))

res.collect()
res.saveAsTextFile("my_output")
