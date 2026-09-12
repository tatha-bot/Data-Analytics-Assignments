# Hadoop Quick Reference Guide

To run Hadoop jobs successfully on your system, you generally go through a standard workflow: starting the cluster, preparing your data on HDFS, compiling your code, running the job, and viewing the results.

Here are the essential commands you need to know from beginning to end.

## 1. Start and Stop Hadoop Services (Distributed Mode)
If you want to run jobs on the Hadoop Distributed File System (HDFS) and use YARN for resource management, you need to start the background services.

* **Start HDFS (NameNode, DataNode):**
  ```bash
  start-dfs.sh
  ```
* **Start YARN (ResourceManager, NodeManager):**
  ```bash
  start-yarn.sh
  ```
* **Start all services at once:**
  ```bash
  start-all.sh
  ```
* **Stop all services:**
  ```bash
  stop-all.sh
  ```
* **Check running Java/Hadoop processes:**
  ```bash
  jps
  ```
  *(You should see NameNode, DataNode, ResourceManager, NodeManager, and SecondaryNameNode)*

---

## 2. Managing Data in HDFS
Before a Hadoop job can process data, the input data must be uploaded from your local Mac filesystem into HDFS.

* **List files in HDFS:**
  ```bash
  hdfs dfs -ls /
  ```
* **Create a directory in HDFS:**
  ```bash
  hdfs dfs -mkdir -p /user/input
  ```
* **Upload a file from Mac to HDFS (put):**
  ```bash
  hdfs dfs -put /path/to/local/file.csv /user/input/
  ```
* **Download a file from HDFS to Mac (get):**
  ```bash
  hdfs dfs -get /user/output/part-r-00000 /path/to/local/folder/
  ```
* **View the contents of a file in HDFS (cat):**
  ```bash
  hdfs dfs -cat /user/output/part-r-00000
  ```
* **Delete a file or folder in HDFS:**
  ```bash
  hdfs dfs -rm -r /user/output
  ```
  *(Note: You **must** delete existing output folders before re-running a job, as Hadoop will not overwrite them).*

---

## 3. Compiling Java MapReduce Code
To run your custom Java MapReduce code, it must be compiled and packaged into a JAR (Java ARchive) file.

* **Export Hadoop Classpath (so Java knows where Hadoop libraries are):**
  ```bash
  export HADOOP_CLASSPATH=$(hadoop classpath)
  ```
* **Compile the Java code:**
  ```bash
  javac -classpath ${HADOOP_CLASSPATH} -d . MyMapReduceProgram.java
  ```
* **Package the compiled `.class` files into a JAR:**
  ```bash
  jar -cvf MyProgram.jar *.class
  ```

---

## 4. Running the MapReduce Job
Once your JAR is ready and your data is in HDFS, you can submit the job.

* **Run on HDFS (Standard):**
  ```bash
  hadoop jar MyProgram.jar MyMainClass /user/input /user/output
  ```
* **Run Locally (Bypass HDFS):**
  *(If your code uses `GenericOptionsParser` (like the one we just fixed), you can force it to run on your local Mac filesystem without starting the Hadoop services).*
  ```bash
  hadoop jar MyProgram.jar MyMainClass -D fs.defaultFS=file:/// -D mapreduce.framework.name=local local_input/ local_output/
  ```

---

## Example End-to-End Workflow

```bash
# 1. Start the cluster
start-all.sh

# 2. Make HDFS directories
hdfs dfs -mkdir -p /input

# 3. Upload data
hdfs dfs -put data.csv /input/

# 4. Compile and package code
export HADOOP_CLASSPATH=$(hadoop classpath)
javac -classpath ${HADOOP_CLASSPATH} -d . WordCount.java
jar -cvf WordCount.jar *.class

# 5. Run the job (Output folder MUST NOT exist yet)
hadoop jar WordCount.jar WordCount /input/data.csv /output

# 6. View Results
hdfs dfs -cat /output/part-r-00000

# 7. Stop the cluster when done
stop-all.sh
```
