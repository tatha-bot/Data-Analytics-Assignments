# Project 1: Install Hadoop and Perform HDFS Tasks

This guide covers the installation of Hadoop on a Mac and the fundamental commands needed to interact with the Hadoop Distributed File System (HDFS). 

## 1. Installing Hadoop on Mac (via Homebrew)
The easiest way to install Hadoop on macOS is by using the Homebrew package manager.

### Prerequisites
Hadoop uses SSH to start and stop its various background processes (NameNode, DataNode, etc.), even if you are only running it locally on a single machine. Therefore, remote login must be enabled.
1. **Enable Remote Login:** Go to **System Settings > General > Sharing** and turn on **Remote Login**.
2. **Setup Passwordless SSH:**
   ```bash
   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   ssh localhost
   ```
   *(If asked to add the host to the known_hosts file, type `yes`).*

### Installation Steps
1. **Install Java (if not already installed):**
   ```bash
   brew install openjdk@11
   ```
2. **Install Hadoop:**
   ```bash
   brew install hadoop
   ```
3. **Configure Hadoop:**
   Hadoop configuration files are usually located at `/opt/homebrew/opt/hadoop/libexec/etc/hadoop/` (on Apple Silicon) or `/usr/local/opt/hadoop/libexec/etc/hadoop/` (on Intel).
   You will need to edit files like `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, and `yarn-site.xml` to set up Pseudo-Distributed mode.
   
4. **Format the NameNode:**
   *(Only do this once, immediately after installation and configuration!)*
   ```bash
   hdfs namenode -format
   ```

---

## 2. Starting Hadoop
Before performing any HDFS tasks, you must ensure that your Hadoop cluster is running.
```bash
# Start all Hadoop daemons (NameNode, DataNode, ResourceManager, NodeManager)
start-all.sh

# Verify that the processes are running
jps
```
*(You should see NameNode, DataNode, ResourceManager, NodeManager, and SecondaryNameNode in the output).*

---

## 3. Basic HDFS Operations

### Creating Directories
To create a new directory inside HDFS, use the `-mkdir` command. The `-p` flag ensures parent directories are created if they don't exist.
```bash
hdfs dfs -mkdir -p /user/hadoop/input
```

### Adding Files to HDFS (Upload)
To copy a file from your local machine into HDFS, use the `-put` or `-copyFromLocal` command.
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

---

## 4. Stopping Hadoop
When you are done with your HDFS tasks, you should safely shut down the Hadoop services.
```bash
stop-all.sh
```
