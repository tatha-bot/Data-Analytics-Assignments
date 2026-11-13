# Question 6: Find Maximum Temperature using Apache Spark (Java Application)

## 📌 Problem Statement
Develop a Java application to find the maximum temperature using Apache Spark.

---

## 💡 Big Data Analytics Approach
In Big Data processing (originally pioneered with the National Climatic Data Center - NCDC weather dataset), temperature records contain meteorological measurements across hundreds of global weather stations. This problem demonstrates key Spark distributed computing concepts:

1. **Distributed Input (`sc.textFile`)**: Loads high-volume sensor records across worker partitions.
2. **Data Cleansing and Filtering**:
   - Removes empty lines, headers, and comments.
   - Parses records from either standard CSV (`Year,Temperature`), whitespace-delimited logs, or raw fixed-width NCDC records.
   - Eliminates missing sensor readings (sentinel values like `9999` or `+9999`).
3. **Map-Reduce Parallel Aggregation (`reduceByKey`)**:
   - Maps raw text lines to key-value pairs: `(Year, Temperature)`.
   - Aggregates by `Year` using `Math::max` across distributed executor nodes.
4. **Global Analytics**:
   - Sorts records chronologically by year (`sortByKey`).
   - Identifies the overall historical maximum temperature and the year it occurred.

---

## 📂 Directory Contents
```
6/
├── MaxTemperature.java       # Java source code using Spark Java API
├── pom.xml                   # Maven project configuration file
├── build_and_run.sh          # One-click build and execution shell script
├── temperatures.txt          # Sample weather dataset (1950 - 2024 + missing values)
├── MaxTemperature.jar        # Pre-built Spark executable JAR
└── README.md                 # Detailed documentation and run guide
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `temperatures.txt` contains 75 years of multi-reading meteorological data with simulated missing sensor markers (`9999.0`).
- **Official Raw NCDC Weather Dataset Sources**:
  1. **NOAA Global Summary of the Day (GSOD)**:  
     URL: [https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/](https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/)
  2. **NOAA FTP Archive**:  
     FTP URL: `ftp://ftp.ncdc.noaa.gov/pub/data/noaa`
  3. **Kaggle Climate Data**:  
     URL: [https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)

---

## 🚀 How to Run

### Method 1: One-Click Runner Script (Recommended)
```bash
cd /Users/mandal/Downloads/6
./build_and_run.sh
```
Or pass a custom dataset path:
```bash
./build_and_run.sh /path/to/custom_weather_data.txt
```

### Method 2: Manual Compilation & `spark-submit`
```bash
cd /Users/mandal/Downloads/6

# Set Spark JARs classpath
SPARK_JARS=$(echo /opt/homebrew/opt/apache-spark/libexec/jars/*.jar | tr ' ' ':')

# Compile
javac -cp "$SPARK_JARS" -d . MaxTemperature.java

# Package into JAR
jar cf MaxTemperature.jar MaxTemperature*.class

# Submit to Spark
spark-submit --class MaxTemperature MaxTemperature.jar temperatures.txt
```

### Method 3: Using Apache Maven
```bash
cd /Users/mandal/Downloads/6
mvn clean package
spark-submit --class MaxTemperature target/spark-max-temperature-1.0.0.jar temperatures.txt
```

---

## 📊 Sample Output
```
===============================================================================
       BIG DATA ANALYTICS: MAXIMUM TEMPERATURE FINDER USING SPARK (JAVA)       
===============================================================================
Loading input file from: temperatures.txt
===============================================================================
Year            | Max Recorded Temp (°C)   
-------------------------------------------------------------------------------
1950            | 37.30                    
1951            | 39.00                    
...
2023            | 43.10                    
2024            | 42.20                    
===============================================================================
OVERALL MAXIMUM TEMPERATURE RECORDED: 43.30 °C in Year 2019
===============================================================================
```
