# Project 1: Install Hadoop and Perform HDFS Tasks

This guide covers the complete end-to-end installation of Hadoop on a Mac and the fundamental commands needed to interact with the Hadoop Distributed File System (HDFS). 

## 1. Full End-to-End Hadoop Installation (Mac via Homebrew)

### Step 1: Enable SSH (Remote Login)
Hadoop uses SSH to start and stop its various background processes (NameNode, DataNode, etc.), even if you are only running it locally on a single machine. 
1. Go to **System Settings > General > Sharing** and turn on **Remote Login**.
2. Open your terminal and set up passwordless SSH:
   ```bash
   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   ssh localhost
   ```
   *(If asked to add the host to the known_hosts file, type `yes`).*

### Step 2: Install Java and Hadoop
Hadoop requires Java to run. We will install Java 11 and Hadoop using Homebrew.
```bash
brew install openjdk@11
brew install hadoop
```

### Step 3: Setup Environment Variables
You need to tell your Mac where to find Java and Hadoop. Open your shell configuration file (usually `~/.zshrc` or `~/.bash_profile`) and add these lines at the bottom:
```bash
# Hadoop & Java Environment Variables
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export HADOOP_HOME=$(brew --prefix hadoop)/libexec
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```
After saving the file, apply the changes by running: `source ~/.zshrc`

### Step 4: Configure Hadoop XML Files
Hadoop's configuration files are located at `$HADOOP_HOME/etc/hadoop`. You need to edit four files to configure Hadoop in "Pseudo-Distributed" mode (running a mini-cluster on a single machine).

**1. `core-site.xml`**
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

**2. `hdfs-site.xml`**
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

**3. `mapred-site.xml`**
```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```

**4. `yarn-site.xml`**
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```

**5. `hadoop-env.sh`**
Inside this file, find the line for `JAVA_HOME` and explicitly set it:
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

### Step 5: Format the NameNode
You must format the filesystem **only once** before you start Hadoop for the very first time.
```bash
hdfs namenode -format
```

---

## 2. Starting Hadoop
Once installation is complete, start your Hadoop cluster:
```bash
# Start all Hadoop daemons
start-all.sh

# Verify that processes are running
jps
```
*(You should see NameNode, DataNode, ResourceManager, NodeManager, and SecondaryNameNode).*

---

## 3. Basic HDFS Operations

### Creating Directories
To create a new directory inside HDFS:
```bash
hdfs dfs -mkdir -p /user/hadoop/input
```

### Adding Files to HDFS (Upload)
To copy a file from your local machine into HDFS:
```bash
echo "Hello Hadoop" > sample.txt
hdfs dfs -put sample.txt /user/hadoop/input/
```

### Listing Files in HDFS
```bash
hdfs dfs -ls /user/hadoop/input/
```

### Reading Files from HDFS
```bash
hdfs dfs -cat /user/hadoop/input/sample.txt
```

### Retrieving Files from HDFS (Download)
```bash
hdfs dfs -get /user/hadoop/input/sample.txt ./downloaded_sample.txt
```

### Deleting Files and Directories
```bash
# Delete a single file
hdfs dfs -rm /user/hadoop/input/sample.txt

# Delete a directory and all its contents
hdfs dfs -rm -r /user/hadoop/input
```

---

## 4. Stopping Hadoop
When you are finished, safely shut down the Hadoop services:
```bash
stop-all.sh
```
