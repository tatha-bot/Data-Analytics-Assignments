#!/usr/bin/env python3
"""
Question 14: Build a Naive Bayes Classifier on a Text Dataset (SMS Spam Detection)
Big Data Analytics Lab Program

Demonstrates:
  1. Distributed Natural Language Processing (NLP) in Apache Spark:
     - RegexTokenizer / Tokenizer
     - StopWordsRemover
     - HashingTF (Term Frequency)
     - IDF (Inverse Document Frequency)
     - StringIndexer
  2. Multinomial Naive Bayes Classification (modelType="multinomial") with Laplace smoothing
  3. Comprehensive Evaluation: Accuracy, Weighted Precision, Weighted Recall, F1-Score, Confusion Matrix
  4. Out-of-Sample Inference: Predicting custom incoming SMS messages
"""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "spam.csv"

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("SMSSpamNaiveBayes") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 80)
    print("      BIG DATA ANALYTICS: SMS SPAM DETECTION VIA SPARK NAIVE BAYES      ")
    print("=" * 80)
    print(f"Loading text dataset from: {dataset_path}")

    # 2. Load dataset
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    df = df.filter(col("message").isNotNull() & col("label").isNotNull())

    total_count = df.count()
    print(f"\n[+] Loaded {total_count} SMS messages.")
    print("\n--- Class Distribution ---")
    df.groupBy("label").count().show()

    # 3. Train / Test Split (80% Train, 20% Test)
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"[+] Train dataset: {train_count} records | Test dataset: {test_count} records")

    # 4. Construct Spark ML Pipeline
    # Stage 1: Label Indexer (maps "ham" -> 0.0, "spam" -> 1.0)
    indexer = StringIndexer(inputCol="label", outputCol="label_index")

    # Stage 2: Regex Tokenizer (splits on non-alphanumeric characters and converts to lower case)
    tokenizer = RegexTokenizer(inputCol="message", outputCol="tokens", pattern="\\W+", toLowercase=True)

    # Stage 3: StopWords Remover (removes common English stop words)
    remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")

    # Stage 4: HashingTF (maps sequence of words to term frequency feature vectors)
    hashing_tf = HashingTF(inputCol="filtered_tokens", outputCol="raw_features", numFeatures=4096)

    # Stage 5: IDF (downweights tokens that appear very frequently across all messages)
    idf = IDF(inputCol="raw_features", outputCol="features")

    # Stage 6: Multinomial Naive Bayes Classifier
    nb = NaiveBayes(featuresCol="features", labelCol="label_index", modelType="multinomial", smoothing=1.0)

    pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashing_tf, idf, nb])

    # 5. Train the Pipeline Model
    print("\n[+] Training Multinomial Naive Bayes Pipeline on Spark...")
    t0 = time.time()
    model = pipeline.fit(train_df)
    train_time = time.time() - t0
    print(f"[+] Model trained in {train_time:.2f} seconds.")

    # 6. Evaluate on Test Dataset
    predictions = model.transform(test_df).cache()

    acc_eval = MulticlassClassificationEvaluator(labelCol="label_index", predictionCol="prediction", metricName="accuracy")
    f1_eval = MulticlassClassificationEvaluator(labelCol="label_index", predictionCol="prediction", metricName="f1")
    prec_eval = MulticlassClassificationEvaluator(labelCol="label_index", predictionCol="prediction", metricName="weightedPrecision")
    rec_eval = MulticlassClassificationEvaluator(labelCol="label_index", predictionCol="prediction", metricName="weightedRecall")

    accuracy = acc_eval.evaluate(predictions)
    f1 = f1_eval.evaluate(predictions)
    precision = prec_eval.evaluate(predictions)
    recall = rec_eval.evaluate(predictions)

    print("\n" + "=" * 80)
    print("                 SMS SPAM CLASSIFICATION PERFORMANCE METRICS            ")
    print("=" * 80)
    print(f"  • Test Accuracy      : {accuracy * 100:.2f}%")
    print(f"  • Weighted Precision : {precision * 100:.2f}%")
    print(f"  • Weighted Recall    : {recall * 100:.2f}%")
    print(f"  • F1-Score           : {f1:.4f}")
    print("=" * 80)

    # Confusion Matrix
    print("\n--- Confusion Matrix ---")
    predictions.groupBy("label", "prediction").count().orderBy("label").show()

    # 7. Real-Time Inference on New Unseen Messages
    print("\n" + "=" * 80)
    print("           REAL-TIME CLASSIFICATION OF SAMPLE INCOMING MESSAGES         ")
    print("=" * 80)

    sample_tests = [
        ("ham", "Hey bro, are we going to the library today for the Big Data revision?"),
        ("spam", "CONGRATULATIONS! You won a $1,000 cash prize or free iPhone 15. Call 0800123456 NOW to claim."),
        ("ham", "Mom asked if you will be home for dinner tonight."),
        ("spam", "URGENT ALERT: Your bank account is suspended due to suspicious activity. Verify credentials at http://bit.ly/secure-login immediately."),
        ("ham", "Can you review my Spark lab code before tomorrow morning?")
    ]

    sample_df = spark.createDataFrame(sample_tests, ["expected_label", "message"])
    sample_preds = model.transform(sample_df).select("message", "prediction", "probability").collect()

    labels = ["ham", "spam"]
    for idx, row in enumerate(sample_preds, 1):
        pred_label = labels[int(row["prediction"])]
        prob_ham = row["probability"][0]
        prob_spam = row["probability"][1]
        print(f"\nMessage {idx}: \"{row['message']}\"")
        print(f"  -> Predicted Label: [{pred_label.upper()}] | Prob(Ham)={prob_ham:.4f}, Prob(Spam)={prob_spam:.4f}")

    print("\n" + "=" * 80)
    spark.stop()


if __name__ == "__main__":
    main()
