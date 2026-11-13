# Question 21: Apply K-Nearest Neighbour (K-NN) Algorithm for Classification of Handwritten Image Dataset

## 📌 Problem Statement
Apply K-Nearest Neighbour algorithm for the classification of handwritten image dataset.

---

## 💡 Big Data Analytics Approach
K-Nearest Neighbour (K-NN) is an instance-based (memory-based) non-parametric machine learning algorithm. Unlike eager learners (e.g., Logistic Regression or Naive Bayes) that compute a fixed parameter set during training, K-NN defers all computation until prediction time.

### Distributed Big Data Architecture on Apache Spark
Running brute-force K-NN on large-scale datasets poses computational bottlenecks ($\mathcal{O}(N_{\text{test}} \times N_{\text{train}} \times D)$). In this Apache Spark implementation:

1. **Broadcast Variable Optimization (`sc.broadcast`)**:
   - The training set is serialized and efficiently distributed to executor memory across all cluster worker nodes.
   - Eliminates redundant network shuffle overhead during query processing.
2. **Parallelized Query Partitions (`test_rdd.mapPartitions`)**:
   - Unseen query images are sliced into distributed partitions.
   - Each worker computes vectorized Euclidean distances concurrently:
     $$d(X_q, X_i) = \sqrt{\sum_{j=1}^{64} (x_{q,j} - x_{i,j})^2}$$
3. **Distributed Top-$K$ Selection & Majority Voting**:
   - For every query image, executors extract the $K$ closest training vectors with minimum Euclidean distances.
   - Computes plurality vote across the $K$ neighbor labels using `collections.Counter`.
4. **Hyperparameter Tuning ($K$-sweep)**:
   - Evaluates performance across $K \in \{1, 3, 5, 7, 9\}$ to identify the optimal bias-variance tradeoff.
   - Generates a full $10 \times 10$ confusion matrix and evaluates classification latency.

---

## 📂 Directory Contents
```
21/
├── knn_spark_images.py       # Distributed PySpark K-NN application
├── run.sh                    # One-click execution shell script
├── digits_knn.csv            # 1,797 handwritten 8x8 digit images (64 pixels each)
└── README.md                 # Documentation, complexity analysis, and run instructions
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `digits_knn.csv` (1,797 handwritten digit images from UCI Optical Recognition of Handwritten Digits).
- **Official Dataset Repositories**:
  1. **UCI Machine Learning Repository - Optical Recognition of Handwritten Digits**:  
     URL: [https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
  2. **Yann LeCun's Official MNIST Database (28x28)**:  
     URL: [http://yann.lecun.com/exdb/mnist/](http://yann.lecun.com/exdb/mnist/)
  3. **Kaggle Digit Recognizer (MNIST)**:  
     URL: [https://www.kaggle.com/c/digit-recognizer](https://www.kaggle.com/c/digit-recognizer)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/21
./run.sh
```
Or specify a custom dataset and $K$ value:
```bash
./run.sh digits_knn.csv 5
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/21
spark-submit --master "local[*]" knn_spark_images.py digits_knn.csv 3
```

---

## 📊 Sample Output
```
=====================================================================================
               RUNNING DISTRIBUTED K-NN PREDICTION (k = 3)              
=====================================================================================
  • Total Test Images Evaluated : 308
  • Correctly Classified        : 304
  • Misclassified               : 4
  • Classification Accuracy     : 98.70%
  • Total Parallel Time         : 0.58 seconds
  • Average Latency per Image   : 1.89 ms
=====================================================================================

=====================================================================================
          K-NN HYPERPARAMETER ANALYSIS: EXPLORING DIFFERENT VALUES OF K        
=====================================================================================
K Value         | Accuracy (%)         | Correct / Total      | Latency (s)    
--------------------------------------------------------------------------------
k = 1           | 99.35                | 306/308                | 0.12           
k = 3           | 98.70                | 304/308                | 0.13           
k = 5           | 98.38                | 303/308                | 0.11           
k = 7           | 98.38                | 303/308                | 0.13           
k = 9           | 98.05                | 302/308                | 0.12           
--------------------------------------------------------------------------------
[+] Optimal Hyperparameter: k = 1 (Accuracy = 99.35%)
=====================================================================================
```
