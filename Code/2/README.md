# Project 2: Word Count using Hadoop MapReduce

This project demonstrates the classic MapReduce "Word Count" algorithm.

## Prerequisites
- Hadoop installed and running.

## Files
- `WordCount.java`: The MapReduce Java code.
- `WordCount.jar`: Compiled JAR for executing the job on Hadoop.

## Execution
1. Create a text file with some words (e.g., `input.txt`) and put it into HDFS:
   ```bash
   hdfs dfs -mkdir /input
   hdfs dfs -put input.txt /input
   ```

2. Run the JAR file:
   ```bash
   hadoop jar WordCount.jar WordCount /input /output
   ```

3. View the output:
   ```bash
   hdfs dfs -cat /output/part-r-00000
   ```
