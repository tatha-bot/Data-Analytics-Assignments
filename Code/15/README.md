# Question 15: Compare Gaussian and Bernoulli Naive Bayes on an Image Dataset

## 📌 Problem Statement
Compare Gaussian and Bernoulli Naive Bayes on an image dataset.

---

## 💡 Big Data Analytics Approach
Naive Bayes classifiers differ fundamentally based on the parametric distribution assumed for feature likelihoods:

### 1. Gaussian Naive Bayes (`modelType="gaussian"`)
- **Assumption**: Continuous features follow a Gaussian Normal distribution within each class:
  $$P(x_i \mid C_k) = \frac{1}{\sqrt{2\pi\sigma_{k,i}^2}} \exp\left(-\frac{(x_i - \mu_{k,i})^2}{2\sigma_{k,i}^2}\right)$$
- **Pixel Representation**: Continuous grayscale intensities normalized to $[0.0, 1.0]$.
- **Characteristics**: Suitable for smooth continuous variables, but assumes a unimodal bell curve. Pixel values in binary handwriting images are often distinctly bimodal (mostly zero background or high-intensity stroke), which can violate this unimodal assumption.

### 2. Bernoulli Naive Bayes (`modelType="bernoulli"`)
- **Assumption**: Features are independent binary indicators $x_i \in \{0, 1\}$ representing feature presence vs. absence:
  $$P(X \mid C_k) = \prod_{i=1}^d p_{k,i}^{x_i} (1 - p_{k,i})^{(1 - x_i)}$$
- **Pixel Representation**: Images are binarized using Spark's `Binarizer(threshold=0.3)` to indicate ink presence ($1.0$) vs background ($0.0$).
- **Characteristics**: Strongly aligns with the structural morphology of handwritten digits (digit identity is determined by which stroke locations are inked).

---

## 📂 Directory Contents
```
15/
├── compare_gaussian_bernoulli.py  # PySpark script comparing both models
├── run.sh                         # One-click execution shell script
├── digits_images.csv              # 1,797 handwritten 8x8 digit images (64 pixels each)
└── README.md                      # Documentation, comparative analysis, and run guide
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `digits_images.csv` (1,797 samples of 8x8 normalized pixel arrays from UCI Optical Recognition of Handwritten Digits).
- **Official Dataset Repositories**:
  1. **UCI Machine Learning Repository - Optical Recognition of Handwritten Digits**:  
     URL: [https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
  2. **Yann LeCun's Official MNIST Database (28x28 images)**:  
     URL: [http://yann.lecun.com/exdb/mnist/](http://yann.lecun.com/exdb/mnist/)
  3. **Kaggle Digit Recognizer (MNIST)**:  
     URL: [https://www.kaggle.com/c/digit-recognizer](https://www.kaggle.com/c/digit-recognizer)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/15
./run.sh
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/15
spark-submit --master "local[*]" compare_gaussian_bernoulli.py digits_images.csv
```

---

## 📊 Sample Output & Comparison
```
=====================================================================================
        COMPREHENSIVE PERFORMANCE COMPARISON: GAUSSIAN VS. BERNOULLI NAIVE BAYES       
=====================================================================================
Metric                    | Gaussian Naive Bayes      | Bernoulli Naive Bayes    
-------------------------------------------------------------------------------------
Feature Type              | Continuous [0.0 - 1.0]    | Binary {0.0, 1.0}        
Training Time (s)         | 0.3663                    | 0.1615                   
Accuracy (%)              | 81.17                     | 89.61                    
Weighted Precision (%)    | 86.76                     | 90.21                    
Weighted Recall (%)       | 81.17                     | 89.61                    
F1-Score                  | 0.8188                    | 0.8970                   
=====================================================================================
```
