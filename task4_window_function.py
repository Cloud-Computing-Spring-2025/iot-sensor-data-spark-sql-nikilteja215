from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, dense_rank
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("IoT Sensor Task 4").getOrCreate()
df = spark.read.option("header", True).option("inferSchema", True).csv("sensor_data.csv")

avg_df = df.groupBy("sensor_id").agg(avg("temperature").alias("avg_temp"))

windowSpec = Window.orderBy(avg_df["avg_temp"].desc())
ranked = avg_df.withColumn("rank_temp", dense_rank().over(windowSpec))

ranked.limit(5).write.mode("overwrite").csv("task4_output.csv", header=True)
