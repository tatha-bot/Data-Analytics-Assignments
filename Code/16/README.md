# Question 16: Implement Bayes’ Theorem for Multiclass Classification using an Image Dataset

## 📌 Problem Statement
Implement Bayes’ Theorem for multiclass classification using an image dataset.

---

## 💡 Big Data Analytics Approach
Multiclass classification via Bayes' Theorem extends the two-class formulation across $K = 10$ distinct classes ($C_k \in \{0, 1, 2, \dots, 9\}$):

### 1. Multiclass Maximum A Posteriori (MAP) Decision Rule
For an image with pixel vector $X = (x_1, x_2, \dots, x_d)$:

$$\hat{y} = \arg\max_{k \in \{0, \dots, 9\}} P(C_k \mid X) = \arg\max_{k \in \{0, \dots, 9\}} \frac{P(C_k) \prod_{j=1}^d P(x_j \mid C_k)}{P(X)}$$

Because $P(X) = \sum_{m=0}^9 P(C_m) P(X \mid C_m)$ is constant across all candidate classes for a given test image, the classification decision reduces to maximizing the numerator in log space:

$$\hat{y} = \arg\max_{k \in \{0, \dots, 9\}} \left[ \ln P(C_k) + \sum_{j=1}^d \ln P(x_j \mid C_k) \right]$$

### 2. Implementation Pipeline on Apache Spark
- **Distributed Prior Estimation**: Calculates prior probability $P(C_k) = \frac{N_k}{N_{\text{total}}}$ for all 10 classes in parallel.
- **MinMax Pixel Scaling**: Normalizes pixel intensities across all 64 image dimensions into $[0.0, 1.0]$.
- **Spark MLlib `NaiveBayes(modelType="multinomial")`**: Trains model parameters across executor nodes with Laplace smoothing ($\lambda = 1.0$).
- **Comprehensive Multiclass Evaluation**: Evaluates overall Accuracy, Precision, Recall, F1-Score, and a complete $10 \times 10$ confusion matrix.
- **Posterior Probability Inspection**: Visualizes full posterior probability vectors $P(C_k \mid X)$ across all 10 digits for individual test images.

---

## 📂 Directory Contents
```
16/
├── bayes_multiclass_images.py  # PySpark multiclass classification script
├── run.sh                      # One-click execution shell script
├── digits_multiclass.csv       # 1,797 handwritten 8x8 digit images (classes 0-9)
└── README.md                   # Theory, mathematical formulation, and run instructions
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `digits_multiclass.csv` (1,797 handwritten digit images with 64 pixel features each, from UCI Optical Recognition of Handwritten Digits).
- **Official Dataset Repositories**:
  1. **UCI Machine Learning Repository - Optical Recognition of Handwritten Digits**:  
     URL: [https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
  2. **Yann LeCun's Official MNIST Database (28x28)**:  
     URL: [http://yann.lecun.com/exdb/mnist/](http://yann.lecun.com/exdb/mnist/)
  3. **OpenML MNIST_784**:  
     URL: [https://www.openml.org/search?type=data&id=554](https://www.openml.org/search?type=data&id=554)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/16
./run.sh
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/16
spark-submit --master "local[*]" bayes_multiclass_images.py digits_multiclass.csv
```

---

## 📊 Sample Output
```
=====================================================================================
               MULTICLASS BAYESIAN CLASSIFIER EVALUATION REPORT          
=====================================================================================
  • Overall Test Accuracy   : 91.56%
  • Weighted Precision      : 91.95%
  • Weighted Recall         : 91.56%
  • F1-Score                : 0.9168
=====================================================================================

--- 10-Class Confusion Matrix (Actual vs Predicted) ---
+-----+---+---+---+---+---+---+---+---+---+---+
|label|0.0|1.0|2.0|3.0|4.0|5.0|6.0|7.0|8.0|9.0|
+-----+---+---+---+---+---+---+---+---+---+---+
|0.0  |37 |0  |0  |0  |2  |0  |0  |0  |0  |0  |
|1.0  |0  |18 |1  |0  |0  |0  |0  |0  |1  |2  |
|2.0  |0  |1  |39 |0  |0  |0  |0  |0  |2  |0  |
...
+-----+---+---+---+---+---+---+---+---+---+---+
```
