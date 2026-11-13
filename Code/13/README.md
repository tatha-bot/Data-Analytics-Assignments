# Question 13: Implement Bayes’ Theorem for Two-Class Classification using Iris Dataset

## 📌 Problem Statement
Implement Bayes’ Theorem for two-class classification using Iris dataset.

---

## 💡 Big Data Analytics Approach
Bayes' Theorem is the cornerstone of statistical pattern recognition. This program delivers both a **first-principles mathematical derivation** executed through distributed Spark transformations and a **production-grade Spark MLlib implementation**.

### 1. Mathematical Formulation
Given an observation vector $X = (x_1, x_2, \dots, x_d)$ and classes $C_k \in \{\text{setosa}, \text{versicolor}\}$:

$$\text{Posterior: } P(C_k \mid X) = \frac{P(C_k) \cdot P(X \mid C_k)}{P(X)} = \frac{P(C_k) \cdot \prod_{j=1}^d P(x_j \mid C_k)}{\sum_m P(C_m) \cdot \prod_{j=1}^d P(x_j \mid C_m)}$$

- **Class Prior $P(C_k)$**: Computed across Spark partitions as the class frequency ratio $\frac{N_k}{N_{\text{total}}}$.
- **Gaussian Likelihood $P(x_j \mid C_k)$**: Continuous floral measurements are modeled using the Gaussian normal distribution:
  $$P(x_j \mid \mu_{k,j}, \sigma_{k,j}) = \frac{1}{\sqrt{2\pi\sigma_{k,j}^2}} \exp\left(-\frac{(x_j - \mu_{k,j})^2}{2\sigma_{k,j}^2}\right)$$
  where $\mu_{k,j}$ and $\sigma_{k,j}^2$ are computed via Spark distributed aggregations (`avg` and `stddev_pop`).

### 2. Apache Spark MLlib Pipeline
- Uses `StringIndexer` to encode class labels into numeric indices.
- Uses `VectorAssembler` to assemble continuous features (`sepal_length`, `sepal_width`, `petal_length`, `petal_width`).
- Trains `pyspark.ml.classification.NaiveBayes(modelType="gaussian")`.
- Evaluates using `MulticlassClassificationEvaluator` across Accuracy, Precision, Recall, and F1-Score.

---

## 📂 Directory Contents
```
13/
├── bayes_two_class.py        # PySpark script (First-principles Bayes + Spark MLlib)
├── run.sh                    # One-click execution shell script
├── iris.csv                  # Standard Iris dataset (150 instances)
└── README.md                 # Mathematical theory and execution instructions
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `iris.csv` (150 rows: Sepal Length, Sepal Width, Petal Length, Petal Width, Species).
- **Official Dataset Repositories**:
  1. **UCI Machine Learning Repository - Iris**:  
     URL: [https://archive.ics.uci.edu/dataset/53/iris](https://archive.ics.uci.edu/dataset/53/iris)
  2. **Kaggle Iris Dataset**:  
     URL: [https://www.kaggle.com/datasets/uciml/iris](https://www.kaggle.com/datasets/uciml/iris)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/13
./run.sh
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/13
spark-submit --master "local[*]" bayes_two_class.py iris.csv
```

---

## 📊 Sample Output
```
--- 1. Class Priors P(C) ---
    P(Species = 'versicolor') = 0.5422
    P(Species = 'setosa') = 0.4578

--- 2. Learned Gaussian Parameters per Class ---
versicolor: sepal_len: 5.97 (std 0.52), petal_len: 4.23 (std 0.47)
setosa    : sepal_len: 5.00 (std 0.34), petal_len: 1.47 (std 0.17)

--- 3. Evaluating Bayes' Theorem on Unseen Test Set ---
Actual       | P(setosa|X)     | P(versicolor|X) | Predicted    | Match?
-----------------------------------------------------------------
setosa       | 1.000000        | 0.000000        | setosa       | ✓
versicolor   | 0.000000        | 1.000000        | versicolor   | ✓
...
[+] Mathematical Bayes' Theorem Test Accuracy: 100.00% (17/17)

================================================================================
                SPARK MLlib NAIVE BAYES EVALUATION SUMMARY              
================================================================================
  • Accuracy           : 100.00%
  • Weighted Precision : 100.00%
  • Weighted Recall    : 100.00%
  • F1-Score           : 1.0000
================================================================================
```
