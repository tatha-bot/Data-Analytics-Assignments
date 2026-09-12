# Data Analytics Assignments

This repository contains various Hadoop and Data Analytics programs. 

## Project 1: Install Hadoop and Perform HDFS Tasks (Mac via Homebrew)

### Prerequisites
- Homebrew installed on your Mac.
- Java (JDK) installed (Hadoop requires Java).

### Installation Steps
1. **Install Hadoop using Homebrew**:
   ```bash
   brew install hadoop
   ```

2. **Configure Hadoop**:
   Open `/opt/homebrew/opt/hadoop/libexec/etc/hadoop/hadoop-env.sh` (or `/usr/local/...` for Intel Macs) and set `JAVA_HOME`.
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home)
   ```

3. **Configure `core-site.xml`**:
   Edit `core-site.xml` located in the Hadoop config directory to add:
   ```xml
   <configuration>
       <property>
           <name>fs.defaultFS</name>
           <value>hdfs://localhost:9000</value>
       </property>
   </configuration>
   ```

4. **Configure `hdfs-site.xml`**:
   Edit `hdfs-site.xml` to add:
   ```xml
   <configuration>
       <property>
           <name>dfs.replication</name>
           <value>1</value>
       </property>
   </configuration>
   ```

5. **Format NameNode** (Do this only once):
   ```bash
   hdfs namenode -format
   ```

6. **Start Hadoop Services**:
   ```bash
   start-dfs.sh
   start-yarn.sh
   ```

### Basic HDFS Tasks
- **Create a directory**: `hdfs dfs -mkdir /my_directory`
- **Upload a file**: `hdfs dfs -put local_file.txt /my_directory/`
- **Read file content**: `hdfs dfs -cat /my_directory/local_file.txt`
- **Download a file**: `hdfs dfs -get /my_directory/local_file.txt ./`
- **Delete a file**: `hdfs dfs -rm /my_directory/local_file.txt`

## Other Projects Included
- **[Project 2](Code/2/)**: Word Count using Hadoop MapReduce
- **[Project 3](Code/3/)**: Matrix Multiplication using Hadoop MapReduce
- **[Project 4](Code/4/)**: Find tags associated with each movie (MovieLens dataset)

