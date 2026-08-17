# Project 4: Find Movie Tags

This MapReduce program extracts and processes tags associated with movies, likely using the MovieLens dataset.

## Files
- `MovieTags.java`: The MapReduce code to process tags.

## Execution (If compiled to JAR)
1. Upload the `tags.csv` file from the MovieLens dataset to HDFS:
   ```bash
   hdfs dfs -put tags.csv /movielens/tags.csv
   ```

2. Run the MapReduce Job:
   ```bash
   hadoop jar movietags.jar MovieTags /movielens/tags.csv /output_tags
   ```

3. Check the output:
   ```bash
   hdfs dfs -cat /output_tags/part-r-00000
   ```
