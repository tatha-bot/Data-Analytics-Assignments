# Data Analytics & Big Data Assignments

A complete collection of **Hadoop MapReduce**, **HDFS**, **Apache Hive**, and **Apache Spark (Java & PySpark)** assignments—ranging from cluster installation and distributed storage to classical Big Data algorithms and distributed Machine Learning.

---

## Table of Contents
1. [Prerequisites & macOS End-to-End Setup](#prerequisites--macos-end-to-end-setup)
   - [1. Install Homebrew & Xcode CLI Tools](#1-install-homebrew--xcode-cli-tools)
   - [2. Enable Passwordless SSH (for Hadoop)](#2-enable-passwordless-ssh-for-hadoop)
   - [3. Install Java, Hadoop, Hive, Spark & Python](#3-install-java-hadoop-hive-spark--python)
   - [4. Configure Environment Variables (`~/.zshrc`)](#4-configure-environment-variables-zshrc)
   - [5. Configure Hadoop (Pseudo-Distributed Mode)](#5-configure-hadoop-pseudo-distributed-mode)
   - [6. Initialize & Start Services](#6-initialize--start-services)
2. [Assignments & Projects Directory](#assignments--projects-directory)
   - [Hadoop & Hive Projects (1–5)](#hadoop--hive-projects-15)
   - [Apache Spark Projects (6, 7, 13–16, 21)](#apache-spark-projects-6-7-1316-21)
3. [Quick Start: Running Any Assignment](#quick-start-running-any-assignment)
4. [Common Troubleshooting (macOS)](#common-troubleshooting-macos)

---

## Prerequisites & macOS End-to-End Setup

Follow these steps in order to set up a complete Big Data environment on **macOS** (Apple Silicon or Intel) using Homebrew.

### 1. Install Homebrew & Xcode CLI Tools
```bash
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Enable Passwordless SSH (for Hadoop)
Hadoop uses SSH to manage its local daemons (NameNode, DataNode, ResourceManager, NodeManager).
1. Open **System Settings > General > Sharing** and turn on **Remote Login**.
2. Generate an SSH key and authorize `localhost`:
   ```bash
   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ssh localhost
   ```
   *(Type `yes` if prompted to add `localhost` to `known_hosts`, then `exit`.)*

### 3. Install Java, Hadoop, Hive, Spark & Python
```bash
brew install openjdk@11
brew install hadoop
brew install hive
brew install apache-spark
brew install maven        # Optional: for building Java/Spark projects with pom.xml
brew install python
```

Link OpenJDK so macOS Java wrappers can find it:
```bash
sudo ln -sfn "$(brew --prefix)/opt/openjdk@11/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

Install Python packages used by the PySpark ML scripts (if running outside `spark-submit`'s bundled Python or using `numpy`):
```bash
pip3 install numpy pyspark
```

### 4. Configure Environment Variables (`~/.zshrc`)
Add the following to `~/.zshrc` (works on both Apple Silicon `/opt/homebrew` and Intel `/usr/local`):
```bash
# Java
export JAVA_HOME=$(/usr/libexec/java_home -v 11)

# Hadoop
export HADOOP_HOME=$(brew --prefix hadoop)/libexec
export HADOOP_CONF_DIR="$HADOOP_HOME/etc/hadoop"
export PATH="$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin"

# Hive
export HIVE_HOME=$(brew --prefix hive)/libexec
export PATH="$PATH:$HIVE_HOME/bin"

# Apache Spark
export SPARK_HOME=$(brew --prefix apache-spark)/libexec
export PATH="$PATH:$SPARK_HOME/bin"
export PYSPARK_PYTHON=$(which python3)
```
Reload your shell configuration:
```bash
source ~/.zshrc
```

### 5. Configure Hadoop (Pseudo-Distributed Mode)
Edit the XML files inside `$HADOOP_HOME/etc/hadoop`:

1. **`core-site.xml`**
   ```xml
   <configuration>
       <property>
           <name>fs.defaultFS</name>
           <value>hdfs://localhost:9000</value>
       </property>
   </configuration>
   ```

2. **`hdfs-site.xml`**
   ```xml
   <configuration>
       <property>
           <name>dfs.replication</name>
           <value>1</value>
       </property>
   </configuration>
   ```

3. **`mapred-site.xml`**
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

4. **`yarn-site.xml`**
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

5. **`hadoop-env.sh`** — uncomment/set `JAVA_HOME`:
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home -v 11)
   ```

### 6. Initialize & Start Services
Format the HDFS NameNode **once** before first use:
```bash
hdfs namenode -format
```

Start Hadoop (HDFS + YARN) and verify daemons:
```bash
start-all.sh
jps
```
You should see `NameNode`, `DataNode`, `SecondaryNameNode`, `ResourceManager`, and `NodeManager`.

*(Optional, for Assignment 5)* Initialize Hive's local Derby metastore once:
```bash
schematool -dbType derby -initSchema
```

When finished with Hadoop services, stop them cleanly with:
```bash
stop-all.sh
```

---

## Assignments & Projects Directory

All assignments live under [`Code/`](./Code).

### Hadoop & Hive Projects (1–5)

| # | Project | Tech Stack | Guide / Source |
|---|---------|-----------|----------------|
| **1** | **Hadoop Installation & HDFS Tasks** — End-to-end macOS Hadoop setup and HDFS CLI cheat sheet (`mkdir`, `put`, `ls`, `cat`, `get`, `rm`). | Hadoop / HDFS | [Code/1/README.md](./Code/1/README.md) |
| **2** | **MapReduce Word Count** — Classic distributed Word Count using Hadoop's built-in example or custom Java Mapper/Reducer. | Java / MapReduce | [Code/2/README.md](./Code/2/README.md) |
| **3** | **Matrix Multiplication** — Sparse coordinate (`A,i,j,val` / `B,j,k,val`) distributed matrix multiplication via Hadoop Configuration parameters. | Java / MapReduce | [Code/3/README.md](./Code/3/README.md) |
| **4** | **Movie Tags Extraction** — Processes MovieLens `tags.csv` and groups all user tags per `movieId`. | Java / MapReduce | [Code/4/README.md](./Code/4/README.md) |
| **5** | **HiveQL Sorting & Aggregation** — Creates `sales_records`, loads `data.csv`, and runs `GROUP BY`, `AVG`/`MAX`, `ORDER BY`, `SORT BY`, and `HAVING` queries. | Apache Hive | [Code/5/hive_queries.hql](./Code/5/hive_queries.hql) |

### Apache Spark Projects (6, 7, 13–16, 21)

| # | Project | Tech Stack | Guide / Runner |
|---|---------|-----------|----------------|
| **6** | **Maximum Temperature Finder** — Parses CSV, whitespace, and NCDC weather records, filters sentinel values (`9999`), and computes max temp per year & overall max. | Spark (Java) | [Code/6/README.md](./Code/6/README.md) / [`build_and_run.sh`](./Code/6/build_and_run.sh) |
| **7** | **Clustering Techniques** — Compares K-Means, Bisecting K-Means, and Gaussian Mixture Models (GMM) with `StandardScaler` & Silhouette Elbow analysis. | PySpark MLlib | [Code/7/README.md](./Code/7/README.md) / [`run.sh`](./Code/7/run.sh) |
| **13** | **Bayes' Theorem (Two-Class Iris)** — First-principles Gaussian Bayes' Theorem via Spark aggregations alongside `NaiveBayes(modelType="gaussian")`. | PySpark MLlib | [Code/13/README.md](./Code/13/README.md) / [`run.sh`](./Code/13/run.sh) |
| **14** | **SMS Spam Detection** — NLP pipeline (`RegexTokenizer` -> `StopWordsRemover` -> `HashingTF` -> `IDF` -> Multinomial Naive Bayes) with live message predictions. | PySpark MLlib | [Code/14/README.md](./Code/14/README.md) / [`run.sh`](./Code/14/run.sh) |
| **15** | **Gaussian vs. Bernoulli Naive Bayes (Images)** — Compares continuous vs. binarized pixel models on handwritten digit images. | PySpark MLlib | [Code/15/README.md](./Code/15/README.md) / [`run.sh`](./Code/15/run.sh) |
| **16** | **Multiclass Bayes' Theorem (Digits)** — 10-class MAP digit classification with log-space posterior probability inspection and confusion matrix. | PySpark MLlib | [Code/16/README.md](./Code/16/README.md) / [`run.sh`](./Code/16/run.sh) |
| **21** | **Distributed K-NN (Handwritten Digits)** — Broadcasted training vectors + `mapPartitions` Euclidean distance + hyperparameter sweep ($k \in \{1,3,5,7,9\}$). | PySpark RDD | [Code/21/README.md](./Code/21/README.md) / [`run.sh`](./Code/21/run.sh) |

---

## Quick Start: Running Any Assignment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tatha-bot/Data-Analytics-Assignments.git
   cd Data-Analytics-Assignments
   ```

2. **Run Hadoop MapReduce Assignments (`Code/2`, `3`, `4`):**
   Ensure HDFS/YARN is running (`start-all.sh`), then follow each folder's `README.md` to compile (if needed), upload data to HDFS, and run `hadoop jar ...`.

3. **Run Hive Assignment (`Code/5`):**
   Update the `LOAD DATA LOCAL INPATH` path in `Code/5/hive_queries.hql` if needed, then run:
   ```bash
   cd Code/5
   hive -f hive_queries.hql
   ```

4. **Run Spark Java Assignment (`Code/6`):**
   ```bash
   cd Code/6
   chmod +x build_and_run.sh
   ./build_and_run.sh
   ```

5. **Run PySpark Assignments (`Code/7`, `13`, `14`, `15`, `16`, `21`):**
   ```bash
   cd Code/<Number>
   chmod +x run.sh
   ./run.sh
   ```

---

## Common Troubleshooting (macOS)

- **`PATH_NOT_FOUND: hdfs://localhost:9000/user/<user>/...` in Spark:**  
  When Hadoop is configured with `fs.defaultFS = hdfs://localhost:9000`, Spark interprets bare relative filenames as HDFS paths. The `run.sh` and `build_and_run.sh` scripts automatically resolve local files to `file:///...` URIs; if invoking `spark-submit` manually, pass `file://$(pwd)/<dataset>.csv`.
- **`Output directory ... already exists` in Hadoop:**  
  MapReduce refuses to overwrite existing HDFS output folders. Delete the output folder before re-running:
  ```bash
  hdfs dfs -rm -r /output
  ```
- **NameNode in Safe Mode:**  
  If HDFS stays in safe mode after startup:
  ```bash
  hdfs dfsadmin -safemode leave
  ```
- **Spark Web UI / Port Conflicts:**  
  Spark runs locally on `local[*]` and binds its UI to port `4040` (auto-incrementing if busy).
