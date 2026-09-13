# Project 2: Word Count using Hadoop MapReduce

This project demonstrates the classic MapReduce "Word Count" algorithm.

## Files
- `WordCount.java`: The custom MapReduce Java code.
- `input.txt`: A sample text file to test the word count.

---

## Method 1: Using Hadoop's Built-in Example (Recommended)
Hadoop comes with a pre-compiled `wordcount` example that you can run without needing to compile any Java code yourself.

### 1. Start Hadoop Services
```bash
start-all.sh
```

### 2. Prepare Data in HDFS
```bash
# Create an input directory in HDFS
hdfs dfs -mkdir -p /input

# Upload the sample text file
hdfs dfs -put input.txt /input/
```

### 3. Run the Built-in WordCount Job
Hadoop stores its example JARs in its installation directory. You can run the built-in word count like this:
```bash
# Delete old output directory if it exists
hdfs dfs -rm -r /output

# Run the built-in wordcount example
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /input/input.txt /output
```

### 4. View Results
```bash
hdfs dfs -cat /output/part-r-00000
```

---

## Method 2: Compiling and Running the Custom Code
If you want to run the custom `WordCount.java` file instead of the built-in one, follow these steps:

### 1. Compile the Java Code
```bash
export HADOOP_CLASSPATH=$(hadoop classpath)
javac -classpath ${HADOOP_CLASSPATH} -d . WordCount.java
jar -cvf WordCount.jar *.class
```

### 2. Run the Custom Job
Assuming your Hadoop services are running and your data is already in HDFS (as shown in Method 1):
```bash
hdfs dfs -rm -r /output
hadoop jar WordCount.jar WordCount /input/input.txt /output
```

### 3. View Results
```bash
hdfs dfs -cat /output/part-r-00000
```
