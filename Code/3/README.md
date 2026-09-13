# Project 3: Matrix Multiplication using Hadoop MapReduce

This project demonstrates how to perform Matrix Multiplication using a Hadoop MapReduce job. 

## Files
- `MatrixMultiplication.java`: The Java source code containing the Mapper and Reducer logic for multiplying two matrices.
- `matrix.txt`: The input file representing two matrices (A and B) in a sparse coordinate format (`MatrixName,row,col,value`).

## Step-by-Step Execution (From Scratch)

Follow these steps to compile and run the project for the first time. Open your terminal and navigate to the `Code/3` directory.

### 1. Compile the Java Code
First, compile the Java source and package it into a JAR file so Hadoop can execute it:
```bash
export HADOOP_CLASSPATH=$(hadoop classpath)
javac -classpath ${HADOOP_CLASSPATH} -d . MatrixMultiplication.java
jar -cvf Matrix.jar *.class
```

### 2. Start Hadoop Services
Ensure your Hadoop cluster (HDFS and YARN) is running:
```bash
start-all.sh
```

### 3. Prepare Data in HDFS
Create an input directory in HDFS and upload the `matrix.txt` file:
```bash
# Create the input directory in HDFS
hdfs dfs -mkdir -p /matrix_input

# Upload matrix.txt from your local machine to HDFS
hdfs dfs -put matrix.txt /matrix_input/matrix.txt
```

### 4. Run the MapReduce Job
The program expects 5 arguments: `<input_dir> <output_dir> <m> <n> <p>`
Where:
- `m`: Number of rows in Matrix A
- `n`: Number of columns in Matrix A (which is also the number of rows in Matrix B)
- `p`: Number of columns in Matrix B

Based on the provided `matrix.txt`, Matrix A is a 2x3 matrix and Matrix B is a 3x2 matrix. So `m=2`, `n=3`, `p=2`.

```bash
# Delete the old output directory (if it exists)
hdfs dfs -rm -r /matrix_output

# Run the map-reduce job
hadoop jar Matrix.jar MatrixMultiplication /matrix_input /matrix_output 2 3 2
```

### 5. View the Results
Once the job finishes successfully, view the resulting Matrix C:
```bash
hdfs dfs -cat /matrix_output/part-r-00000
```
The output format will be `row,col,value` representing the computed Matrix C.

*(When you are completely finished testing, you can stop your Hadoop services using `stop-all.sh`).*
