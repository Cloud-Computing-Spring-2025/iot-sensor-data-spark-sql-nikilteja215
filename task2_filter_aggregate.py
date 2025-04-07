from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("IoT Sensor Task 2").getOrCreate()
df = spark.read.option("header", True).option("inferSchema", True).csv("sensor_data.csv")

in_range = df.filter((df.temperature >= 18) & (df.temperature <= 30))
out_of_range = df.filter((df.temperature < 18) | (df.temperature > 30))

print("In-range count:", in_range.count())
print("Out-of-range count:", out_of_range.count())

agg = df.groupBy("location").avg("temperature", "humidity") \
        .withColumnRenamed("avg(temperature)", "avg_temperature") \
        .withColumnRenamed("avg(humidity)", "avg_humidity") \
        .orderBy("avg_temperature", ascending=False)

agg.write.mode("overwrite").csv("task2_output.csv", header=True)
