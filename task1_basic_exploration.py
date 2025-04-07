from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("IoT Sensor Task 1").getOrCreate()

# Load CSV with schema inference
df = spark.read.option("header", True).option("inferSchema", True).csv("sensor_data.csv")

# Create a temporary view
df.createOrReplaceTempView("sensor_readings")

# Show first 5 rows
df.show(5)

# Total number of records
print("Total records:", df.count())

# Distinct locations
df.select("location").distinct().show()

# ✅ Save only the first 5 rows to CSV
df.limit(5).write.mode("overwrite").csv("task1_output.csv", header=True)
