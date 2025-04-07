from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, avg, to_timestamp, round as spark_round

spark = SparkSession.builder.appName("IoT Sensor Task 5").getOrCreate()
df = spark.read.option("header", True).option("inferSchema", True).csv("sensor_data.csv")

# Convert timestamp and extract hour
df = df.withColumn("timestamp", to_timestamp("timestamp"))
df = df.withColumn("hour_of_day", hour("timestamp"))

# Create pivot table
pivot_df = df.groupBy("location").pivot("hour_of_day").agg(avg("temperature"))

# Round all hour columns to 2 decimal places
for col_name in pivot_df.columns[1:]:  # Skip "location"
    pivot_df = pivot_df.withColumn(col_name, spark_round(col_name, 2))

# Write to CSV
pivot_df.write.mode("overwrite").csv("task5_output.csv", header=True)
