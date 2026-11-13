# Question 14: Build a Naive Bayes Classifier on a Text Dataset (SMS Spam Detection)

## 📌 Problem Statement
Build a Naive Bayes Classifier on a text dataset (e.g., SMS spam detection).

---

## 💡 Big Data Analytics Approach
Text categorization in distributed environments requires a multi-stage feature extraction and transformation pipeline before applying machine learning. In this Apache Spark implementation:

1. **Text Cleansing & Tokenization (`RegexTokenizer`)**:
   - Converts raw unstructured text messages to lowercase.
   - Splits on regular expression `\W+` to isolate individual word tokens.
2. **Stop-Word Removal (`StopWordsRemover`)**:
   - Strips common, non-discriminative English terms (e.g., "the", "is", "at", "in").
3. **Term Frequency Hashing (`HashingTF`)**:
   - Applies the MurmurHash 3 algorithm to project variable-length word tokens into a fixed-size numerical feature vector ($N = 4096$).
4. **Inverse Document Frequency Weighting (`IDF`)**:
   - Scales feature dimensions such that words occurring across many documents receive lower weights, emphasizing rare, highly descriptive spam/ham terms.
5. **Multinomial Naive Bayes (`NaiveBayes(modelType="multinomial")`)**:
   - Uses Laplace add-one smoothing ($\lambda = 1.0$) to prevent zero-probability errors on unseen test vocabulary:
     $$P(w_i \mid C_k) = \frac{N_{ki} + \alpha}{N_k + \alpha \cdot |V|}$$

---

## 📂 Directory Contents
```
14/
├── sms_spam_naive_bayes.py   # Complete PySpark NLP & classification pipeline
├── run.sh                    # One-click execution shell script
├── spam.csv                  # Full SMS Spam Collection dataset (5,574 messages)
└── README.md                 # Documentation, pipeline details, and run instructions
```

---

## 🌐 Dataset Information & Download Links
- **Included Dataset**: `spam.csv` (5,574 genuine and spam text messages from the UCI Machine Learning Repository).
- **Official Dataset Repositories**:
  1. **UCI Machine Learning Repository - SMS Spam Collection**:  
     URL: [https://archive.ics.uci.edu/dataset/228/sms+spam+collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
  2. **Kaggle SMS Spam Collection**:  
     URL: [https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)

---

## 🚀 How to Run

### Method 1: Using the Runner Script
```bash
cd /Users/mandal/Downloads/14
./run.sh
```

### Method 2: Direct `spark-submit`
```bash
cd /Users/mandal/Downloads/14
spark-submit --master "local[*]" sms_spam_naive_bayes.py spam.csv
```

---

## 📊 Sample Output
```
[+] Loaded 5574 SMS messages.
--- Class Distribution ---
+-----+-----+
|label|count|
+-----+-----+
|  ham| 4827|
| spam|  747|
+-----+-----+

================================================================================
                 SMS SPAM CLASSIFICATION PERFORMANCE METRICS            
================================================================================
  • Test Accuracy      : 93.46%
  • Weighted Precision : 94.63%
  • Weighted Recall    : 93.46%
  • F1-Score           : 0.9381
================================================================================

Real-time sample tests:
  • "CONGRATULATIONS! You won a $1,000 cash prize..." -> [SPAM] (Prob=1.0000)
  • "Hey bro, are we going to the library today..."   -> [HAM]  (Prob=1.0000)
```
