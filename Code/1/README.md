# Project 1: Install Hadoop and Perform HDFS Tasks

This guide covers the basic setup and fundamental commands needed to interact with the Hadoop Distributed File System (HDFS). 

## 1. Starting Hadoop
Before performing any HDFS tasks, you must ensure that your Hadoop cluster is running.
```bash
# Start all Hadoop daemons (NameNode, DataNode, ResourceManager, NodeManager)
start-all.sh

# Verify that the processes are running
jps
```
*(You should see NameNode, DataNode, ResourceManager, NodeManager, and SecondaryNameNode in the output).*

## 2. Basic HDFS Operations

### Creating Directories
To create a new directory inside HDFS, use the `-mkdir` command. The `-p` flag ensures parent directories are created if they don't exist.
```bash
hdfs dfs -mkdir -p /user/hadoop/input
```

### Adding Files to HDFS (Upload)
To copy a file from your local machine (Mac/Linux) into HDFS, use the `-put` or `-copyFromLocal` command.
```bash
# Create a sample local file
echo "Hello Hadoop" > sample.txt

# Upload it to HDFS
hdfs dfs -put sample.txt /user/hadoop/input/
```

### Listing Files in HDFS
To view the contents of a directory in HDFS, use the `-ls` command.
```bash
hdfs dfs -ls /user/hadoop/input/
```

### Reading Files from HDFS
To print the contents of a file stored in HDFS directly to your terminal, use the `-cat` command.
```bash
hdfs dfs -cat /user/hadoop/input/sample.txt
```

### Retrieving Files from HDFS (Download)
To download a file from HDFS back to your local machine, use the `-get` or `-copyToLocal` command.
```bash
# Download the file as 'downloaded_sample.txt'
hdfs dfs -get /user/hadoop/input/sample.txt ./downloaded_sample.txt
```

### Deleting Files and Directories
To delete a file from HDFS, use the `-rm` command. To delete an entire directory and its contents, use `-rm -r`.
```bash
# Delete a single file
hdfs dfs -rm /user/hadoop/input/sample.txt

# Delete a directory and all its contents
hdfs dfs -rm -r /user/hadoop/input
```

## 3. Stopping Hadoop
When you are done with your HDFS tasks, you should safely shut down the Hadoop services.
```bash
stop-all.sh
```
