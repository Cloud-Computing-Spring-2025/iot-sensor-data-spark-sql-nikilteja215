# 📡 IoT Sensor Data Analysis with Spark SQL

This project analyzes simulated IoT sensor data using **PySpark SQL**, applying filtering, aggregation, time-series breakdown, window functions, and pivoting to gain insights on sensor behavior across buildings and time.

---

## 📁 Dataset Overview

**Input File:**
- `sensor_data.csv`

**Schema:**
| Column       | Type      | Description                          |
|--------------|-----------|--------------------------------------|
| `sensor_id`  | Integer   | Unique ID of the sensor              |
| `timestamp`  | Timestamp | Time of the sensor reading           |
| `temperature`| Float     | Temperature recorded (°C)            |
| `humidity`   | Float     | Humidity recorded (%)                |
| `location`   | String    | Sensor location (building/floor)     |
| `sensor_type`| String    | Sensor classification (TypeA/B/C)    |

---

## ✅ Task 1: Load & Basic Exploration

- Load `sensor_data.csv` using Spark
- Create a temporary SQL view `sensor_readings`
- Display:
  - First 5 rows
  - Total record count
  - Distinct locations
- Save the **first 5 records** to `task1_output.csv`

### 🖥 Sample Output:

```text
sensor_id	timestamp	            temperature	humidity	location	        sensor_type
1046	    2025-04-05T23:39:06Z	15.35	      36.92	    BuildingB_Floor1	TypeB
1002	    2025-04-06T21:39:03Z	28.18	      35.86	    BuildingB_Floor1	TypeB
1029	    2025-04-04T22:39:02Z	30.01	      61.66	    BuildingB_Floor1	TypeB
1076	    2025-04-05T15:14:28Z	23.05	      59.53	    BuildingB_Floor2	TypeC
1018	    2025-04-04T07:58:54Z	15.87	      42.13	    BuildingB_Floor1	TypeC
```

### 📊 Analysis:
- Data includes multiple floors and buildings with varied sensor types.
- First few rows help validate schema and data quality.

---

## ✅ Task 2: Filtering & Aggregations

- Filter temperature readings:
  - Count in-range (18–30°C) vs. out-of-range
- Compute average temperature and humidity **by location**

### Output (`task2_output.csv`):

```text
location	        avg_temperature	    avg_humidity
BuildingB_Floor1	25.24	              55.78
BuildingA_Floor2	24.76	              56.42
BuildingB_Floor2	24.36	              54.23
BuildingA_Floor1	24.34	              56.22
```

### 📊 Analysis:
- BuildingB_Floor1 is the warmest and driest.
- Slight humidity variation across floors.

---

## ✅ Task 3: Time-Based Analysis

- Extract `hour_of_day` from timestamps
- Group and average temperatures by hour
- Save to `task3_output.csv`

### Sample Output:

```text
hour_of_day	avg_temp
0	          24.06
1	          24.80
2	          25.76
...
23	        24.17
```

### 📊 Analysis:
- Hours 8 AM to 10 AM and 4–6 PM show slightly higher temperatures.
- Most readings are in the 23–26 °C range, suggesting controlled environments.

---

## ✅ Task 4: Sensor Ranking (Window Function)

- Calculate each sensor’s average temperature
- Apply `dense_rank()` on descending order
- Save top 5 to `task4_output.csv`

### Output:

```text
sensor_id	avg_temp	rank_temp
1002	    29.27	    1
1095	    29.05	    2
1056	    28.73	    3
1026	    28.68	    4
1084	    28.42	    5
```

### 📊 Analysis:
- Sensor 1002 is the hottest on average — may need recalibration or is located in a hotter environment.

---

## ✅ Task 5: Pivot by Hour and Location

- Pivot table with:
  - `location` as rows
  - `hour_of_day` (0–23) as columns
  - `avg(temperature)` in each cell
- Save to `task5_output.csv`

### Sample Output (partial):

```text
location	        0	    1	    2	    ...	    23
BuildingA_Floor1	22.26	25.31	24.59	...	    25.31
BuildingB_Floor2	25.06	23.64	24.90	...	    25.28
BuildingA_Floor2	24.23	24.89	25.90	...	    24.14
BuildingB_Floor1	23.70	25.06	27.23	...	    21.96
```

### 📊 Analysis:
- BuildingA_Floor2 shows highest temps around hours 2–4 and 14–16.
- Useful for HVAC scheduling or identifying overused zones.

---

## ⚙️ How to Run

In **GitHub Codespaces** terminal:

```bash
spark-submit task1_basic_exploration.py
spark-submit task2_filter_aggregate.py
spark-submit task3_time_analysis.py
spark-submit task4_window_function.py
spark-submit task5_pivot_interpretation.py
```

---

## 📁 Output Folder Structure

```
output/
├── task1_output.csv
├── task2_output.csv
├── task3_output.csv
├── task4_output.csv
├── task5_output.csv
```

---

## 🛠️ Problems Faced & Fixes

### ❌ Rounding & Formatting (Task 5)
- **Issue**: Pivot values had too many decimals.
- **Fix**: Used `round(column, 2)` dynamically for all columns post-pivot.

### ❌ Hour-based Sorting in Pivot
- **Issue**: Output CSV did not preserve hour order (0–23).
- **Fix**: Spark handles pivot in correct order if hour column is numeric, ensured hours were casted as `int`.

### ❌ Sensor Ranking Confusion
- Spark window functions required explicit partitioning/ordering. Fixed using `DenseRank().over(Window.orderBy(...))`

---

## 📬 Submission

All `.py` scripts and `.csv` outputs are committed to this GitHub repository.  
Git commands used to push only necessary files:

```bash
git add '*.py'
git add '*.csv'
git add **/*.py
git add **/*.csv'
git commit -m "Add final IoT sensor Spark scripts and outputs"
git push origin main
```

---
