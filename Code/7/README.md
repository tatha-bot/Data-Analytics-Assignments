# Question 7: Implement Clustering Techniques using Apache Spark

## 📌 Problem Statement
Implement clustering techniques using SPARK.

---

## 💡 Big Data Analytics Approach
Clustering is an unsupervised machine learning method that partitions large datasets into distinct groups sharing common features. This implementation showcases three primary distributed clustering paradigms available in Apache Spark MLlib:

1. **Standard K-Means (`pyspark.ml.clustering.KMeans`)**:
   - A partition-based clustering algorithm that minimizes within-cluster sum of squared errors (WSSSE).
   - In distributed Spark, centroid calculation uses parallel map-reduce aggregations across executor partitions.
2. **Bisecting K-Means (`pyspark.ml.clustering.BisectingKMeans`)**:
   - A divisive (top-down) hierarchical clustering technique that begins with one cluster and recursively splits it into two using 2-means.
   - Typically much faster and more scalable than regular K-Means on massive Big Data clusters.
3. **Gaussian Mixture Model (`pyspark.ml.clustering.GaussianMixture`)**:
   - A soft, probabilistic clustering algorithm assuming data points are drawn from a mixture of $k$ multivariate Gaussian distributions.
   - Fits parameters using the distributed Expectation-Maximization (EM) algorithm.

### Preprocessing & Evaluation Pipeline:
- **`VectorAssembler`**: Compiles numerical features into distributed ML vectors.
- **`StandardScaler`**: Scales features to unit standard deviation to avoid domination by large-scale attributes.
- **`ClusteringEvaluator`**: Computes the **Silhouette Score** (range: $[-1, 1]$), where scores near $1.0$ indicate dense, well-separated clusters.
- **Silhouette Elbow Scan**: Explores $k \in [2, 5]$ to quantitatively determine the optimal number of clusters.

---

## 📂 Directory Contents
```
7/
├── clustering_spark.py       # Complete PySpark application code
├── run.sh                    # One-click execution shell script
├── clustering_data.csv       # Multivariate customer spending dataset (300 records)
└── README.md                 # Documentation and execution guide
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `clustering_data.csv` (Customer spending distribution across Fresh, Milk, Grocery, Frozen, Detergents_Paper, and Delicassen categories).
- **Benchmark Real-World Datasets**:
  1. **UCI Wholesale Customers Dataset**:  
     URL: [https://archive.ics.uci.edu/dataset/292/wholesale+customers](https://archive.ics.uci.edu/dataset/292/wholesale+customers)
  2. **Kaggle Mall Customer Segmentation**:  
     URL: [https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python)
  3. **UCI Iris Dataset (Unsupervised)**:  
     URL: [https://archive.ics.uci.edu/dataset/53/iris](https://archive.ics.uci.edu/dataset/53/iris)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/7
./run.sh
```
Or with custom data:
```bash
./run.sh /path/to/custom_data.csv
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/7
spark-submit --master "local[*]" clustering_spark.py clustering_data.csv
```

---

## 📊 Sample Output
```
================================================================================
               CLUSTERING TECHNIQUES PERFORMANCE SUMMARY               
================================================================================
Algorithm                 | Silhouette Score     | Training Time (s) 
--------------------------------------------------------------------------------
K-Means                   | 0.8292               | 1.03              
Bisecting K-Means         | 0.8292               | 0.84              
Gaussian Mixture (GMM)    | 0.8292               | 1.06              
================================================================================

================================================================================
       OPTIMAL k EXPLORATION VIA SILHOUETTE ANALYSIS (K-MEANS)       
================================================================================
k (Number of Clusters)    | Silhouette Score    
--------------------------------------------------
2                         | 0.6350              
3                         | 0.8292              
4                         | 0.6995              
5                         | 0.5681              
--------------------------------------------------
[+] Optimal k based on maximum Silhouette Score: k = 3 (Score: 0.8292)
================================================================================
```
