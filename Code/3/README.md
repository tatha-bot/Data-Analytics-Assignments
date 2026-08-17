# Project 3: Matrix Multiplication using Hadoop MapReduce

This MapReduce application performs Matrix Multiplication.

## Files
- `MatrixMultiplication.java`: MapReduce logic to multiply matrices.
- `Matrix.jar`: The compiled JAR file.

## Execution
1. Prepare your input matrix data in text format.
2. Upload it to HDFS:
   ```bash
   hdfs dfs -put matrix.txt /matrix_input
   ```

3. Run the MapReduce job:
   ```bash
   hadoop jar Matrix.jar MatrixMultiplication /matrix_input /matrix_output
   ```

4. View the resulting matrix:
   ```bash
   hdfs dfs -cat /matrix_output/part-r-00000
   ```
