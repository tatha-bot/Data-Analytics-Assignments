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

## How Each Assignment Works

### Code 1 — Hadoop Installation & HDFS Tasks
- **Goal:** Set up single-node (Pseudo-Distributed) Hadoop on macOS and practice core HDFS operations.
- **How it works:** Configures `core-site.xml` (`fs.defaultFS=hdfs://localhost:9000`), `hdfs-site.xml` (`dfs.replication=1`), `mapred-site.xml` (YARN), and `yarn-site.xml` (`mapreduce_shuffle`), formats the NameNode once, starts daemons via `start-all.sh`, and runs HDFS commands (`mkdir`, `put`, `ls`, `cat`, `get`, `rm`).

### Code 2 — MapReduce Word Count (`WordCount.java`)
- **Goal:** Count word frequencies across text files in HDFS.
- **How it works:**
  1. `TokenizerMapper` splits each input line into tokens with `StringTokenizer` and emits `(word, 1)`.
  2. `IntSumReducer` (used as both Combiner and Reducer) sums the counts per word and outputs `(word, total_count)`.

### Code 3 — Matrix Multiplication (`MatrixMultiplication.java`)
- **Goal:** Multiply two sparse matrices $A_{m \times n}$ and $B_{n \times p}$ in MapReduce.
- **How it works:**
  1. Reads coordinate records `A,i,j,value` and `B,j,k,value` along with dimensions `m`, `n`, `p` passed via Hadoop `Configuration`.
  2. `MatrixMapper` emits `(i,k)` as the key for every output cell affected by `A(i,j)` or `B(j,k)`, tagging values with `"A,j,val"` or `"B,j,val"`.
  3. `MatrixReducer` stores `A` and `B` entries in two `HashMap<Integer, Float>` maps keyed by `j`, computes $\sum_{j=0}^{n-1} A(i,j) \cdot B(j,k)$, and writes non-zero `i,k,result` entries.

### Code 4 — Movie Tags Extraction (`MovieTags.java`)
- **Goal:** Aggregate all user-assigned tags per movie from MovieLens `tags.csv`.
- **How it works:**
  1. `TagMapper` skips the CSV header (`userId,movieId,tag,timestamp`), splits each line, and emits `(movieId, tag)`.
  2. `TagReducer` concatenates all tags for each `movieId` separated by `" | "`.

### Code 5 — HiveQL Sorting & Aggregation (`hive_queries.hql`)
- **Goal:** Create a Hive table from `data.csv` and run analytical SQL queries.
- **How it works:** Defines `sales_records` (`transaction_id`, `product_category`, `sales_amount`, `store_location`), loads `data.csv` with `LOAD DATA LOCAL INPATH`, and executes `GROUP BY` (`SUM`, `COUNT`), global `AVG`/`MAX`, `ORDER BY` (global sort via single reducer), `SORT BY` (per-reducer local sort), and `GROUP BY ... HAVING ... ORDER BY`.

### Code 6 — Maximum Temperature Finder (`MaxTemperature.java`)
- **Goal:** Find the maximum temperature per year and the overall maximum temperature using Spark Java RDDs.
- **How it works:**
  1. Loads `temperatures.txt` with `sc.textFile(...)` and filters out blank/comment/header lines.
  2. `flatMapToPair` parses CSV (`Year,Temp`), whitespace-delimited, or fixed-width NCDC lines and drops invalid/sentinel values (`9999.0`, `999.9`).
  3. `reduceByKey(Math::max)` finds each year's max temperature in parallel, `sortByKey(true)` orders chronologically, and the driver prints the yearly table and overall max.

### Code 7 — Clustering Techniques (`clustering_spark.py`)
- **Goal:** Compare K-Means, Bisecting K-Means, and Gaussian Mixture Models (GMM) on Spark MLlib and find optimal $k$.
- **How it works:**
  1. Loads `clustering_data.csv`, assembles numeric columns with `VectorAssembler`, and scales them with `StandardScaler`.
  2. Fits `KMeans`, `BisectingKMeans`, and `GaussianMixture` with $k=3$, evaluates each with `ClusteringEvaluator` (Silhouette Score), and prints cluster counts.
  3. Runs a Silhouette sweep for $k \in \{2,3,4,5\}$ with `KMeans` to pick the optimal $k$.

### Code 13 — Bayes' Theorem for Two-Class Classification (`bayes_two_class.py`)
- **Goal:** Classify `setosa` vs. `versicolor` in `iris.csv` using both manual Bayes' Theorem and Spark MLlib.
- **How it works:**
  1. Filters `iris.csv` to the two classes and splits 80/20 into train/test.
  2. **Part 1 (First-Principles):** Computes class priors $P(C_k)$ and per-feature Gaussian parameters ($\mu, \sigma$) using distributed Spark `avg` and `stddev_pop` aggregations, then classifies test rows via Gaussian PDF likelihood $\times$ prior.
  3. **Part 2 (Spark MLlib):** Encodes labels with `StringIndexer`, builds feature vectors with `VectorAssembler`, trains `NaiveBayes(modelType="gaussian")`, and prints accuracy, precision, recall, F1, and confusion matrix.

### Code 14 — SMS Spam Detection (`sms_spam_naive_bayes.py`)
- **Goal:** Classify SMS messages as `ham` or `spam` using a Spark NLP + Naive Bayes pipeline.
- **How it works:**
  1. Loads `spam.csv` and splits 80/20 into train/test.
  2. Builds a 6-stage `Pipeline`: `StringIndexer` → `RegexTokenizer` → `StopWordsRemover` → `HashingTF(4096)` → `IDF` → `NaiveBayes(modelType="multinomial", smoothing=1.0)`.
  3. Evaluates accuracy, precision, recall, F1, confusion matrix, and classifies sample incoming messages.

### Code 15 — Gaussian vs. Bernoulli Naive Bayes on Images (`compare_gaussian_bernoulli.py`)
- **Goal:** Compare continuous Gaussian NB against binary Bernoulli NB on 8×8 handwritten digit images (`digits_images.csv`, 64 pixel columns `pixel_0`..`pixel_63`).
- **How it works:**
  1. Assembles the 64 pixels with `VectorAssembler` and normalizes to $[0, 1]$ with `MinMaxScaler` (`features_cont`).
  2. Binarizes normalized pixels at `threshold=0.3` with `Binarizer` (`features_bin`) to capture ink presence vs. background.
  3. Trains `NaiveBayes(modelType="gaussian")` on `features_cont` and `NaiveBayes(modelType="bernoulli")` on `features_bin`, comparing training time and classification metrics.

### Code 16 — Multiclass Bayes' Theorem on Images (`bayes_multiclass_images.py`)
- **Goal:** Perform 10-class (digits `0`–`9`) classification on `digits_multiclass.csv`.
- **How it works:**
  1. Assembles and MinMax-scales the 64 pixel features, then splits 80/20.
  2. Computes and prints class priors $P(C_k)$ for digits `0`–`9` from the training set.
  3. Trains `NaiveBayes(modelType="multinomial", smoothing=1.0)`, evaluates accuracy/precision/recall/F1, prints the 10×10 confusion matrix via `crosstab`, and inspects sample posterior probabilities.

### Code 21 — Distributed K-NN on Images (`knn_spark_images.py`)
- **Goal:** Classify 8×8 handwritten digit images (`digits_knn.csv`) using distributed K-Nearest Neighbours on Spark RDDs.
- **How it works:**
  1. Normalizes the 64 pixel values to $[0, 1]$ and splits 80/20.
  2. Broadcasts the training vectors to all executors using `sc.broadcast(...)` and parallelizes test queries across 4 partitions (`sc.parallelize(..., 4)`).
  3. Inside `mapPartitions`, computes Euclidean distances $\|X_q - X_i\|_2$ with NumPy, picks the $k$ nearest neighbors, and predicts by majority vote (`Counter`).
  4. Sweeps $k \in \{1, 3, 5, 7, 9\}$ to find the best $k$ and prints the 10×10 confusion matrix.

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
