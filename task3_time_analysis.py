from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, avg, to_timestamp

# Create Spark session
spark = SparkSession.builder.appName("IoT Sensor Task 3").getOrCreate()

# Load the CSV
df = spark.read.option("header", True).option("inferSchema", True).csv("sensor_data.csv")

# Convert timestamp string to proper timestamp
df = df.withColumn("timestamp", to_timestamp("timestamp"))

# Create temporary view (optional, still useful)
df.createOrReplaceTempView("sensor_readings")

# Extract hour and group by it
df = df.withColumn("hour_of_day", hour("timestamp"))

# Average temperature per hour, sorted by hour
result = df.groupBy("hour_of_day").agg(avg("temperature").alias("avg_temp")).orderBy("hour_of_day")

# Save to CSV
result.write.mode("overwrite").csv("task3_output.csv", header=True)
