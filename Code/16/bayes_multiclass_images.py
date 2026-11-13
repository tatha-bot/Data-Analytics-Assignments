#!/usr/bin/env python3
"""
Question 16: Implement Bayes' Theorem for Multiclass Classification using an Image Dataset
Big Data Analytics Lab Program

Demonstrates:
  1. Multiclass Bayes' Decision Rule across 10 handwritten digit classes (0-9):
       argmax_{k in {0..9}} [ ln P(C_k) + sum_j ln P(x_j | C_k) ]
  2. Spark MLlib NaiveBayes Pipeline on 64 pixel features.
  3. Comprehensive Multiclass Evaluation:
       - Class Prior Probabilities P(C_0) ... P(C_9)
       - Overall Accuracy, Weighted Precision, Weighted Recall, and F1-Score
       - 10x10 Multiclass Confusion Matrix
       - Detailed posterior probability distribution for sample test digits
"""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_multiclass.csv"

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("BayesMulticlassImages") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 85)
    print("   BIG DATA ANALYTICS: MULTICLASS BAYES' THEOREM CLASSIFIER (DIGIT IMAGES)   ")
    print("=" * 85)
    print(f"Loading image dataset from: {dataset_path}")

    # 2. Load Dataset
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]
    df = df.withColumn("label", col("label").cast("double"))

    total_images = df.count()
    print(f"[+] Total handwritten digit images loaded: {total_images} (64 pixels each)")

    # 3. Assemble and Normalize Features
    assembler = VectorAssembler(inputCols=pixel_cols, outputCol="raw_features")
    df_assembled = assembler.transform(df)

    scaler = MinMaxScaler(inputCol="raw_features", outputCol="features")
    scaler_model = scaler.fit(df_assembled)
    df_scaled = scaler_model.transform(df_assembled).cache()

    # 4. Train / Test Split (80% Train, 20% Test)
    train_df, test_df = df_scaled.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"[+] Train dataset: {train_count} images | Test dataset: {test_count} images")

    # 5. Compute Class Prior Probabilities P(C_k) across all 10 digits
    print("\n--- 1. Learned Class Prior Probabilities P(C_k) from Training Set ---")
    prior_df = train_df.groupBy("label").count().orderBy("label")
    for row in prior_df.collect():
        digit = int(row["label"])
        cnt = row["count"]
        prior_p = cnt / float(train_count)
        print(f"    P(Digit = {digit}) = {prior_p:.4f}  ({cnt}/{train_count} images)")

    # 6. Train Spark MLlib Multinomial / Naive Bayes Model
    print("\n[+] Training Multiclass Naive Bayes Classifier...")
    t0 = time.time()
    nb = NaiveBayes(featuresCol="features", labelCol="label", modelType="multinomial", smoothing=1.0)
    model = nb.fit(train_df)
    train_time = time.time() - t0
    print(f"[+] Model trained in {train_time:.2f} seconds.")

    # 7. Model Evaluation on Unseen Test Images
    predictions = model.transform(test_df).cache()

    acc_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    prec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
    rec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")
    f1_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")

    accuracy = acc_eval.evaluate(predictions)
    precision = prec_eval.evaluate(predictions)
    recall = rec_eval.evaluate(predictions)
    f1 = f1_eval.evaluate(predictions)

    print("\n" + "=" * 85)
    print("               MULTICLASS BAYESIAN CLASSIFIER EVALUATION REPORT          ")
    print("=" * 85)
    print(f"  • Overall Test Accuracy   : {accuracy * 100:.2f}%")
    print(f"  • Weighted Precision      : {precision * 100:.2f}%")
    print(f"  • Weighted Recall         : {recall * 100:.2f}%")
    print(f"  • F1-Score                : {f1:.4f}")
    print("=" * 85)

    # 8. 10x10 Confusion Matrix
    print("\n--- 10-Class Confusion Matrix (Actual vs Predicted) ---")
    conf_df = predictions.groupBy("label").pivot("prediction", [float(i) for i in range(10)]).count().na.fill(0).orderBy("label")
    conf_df.show(10, truncate=False)

    # 9. Step-by-Step Posterior Probabilities for Sample Test Digits
    print("=" * 85)
    print("       STEP-BY-STEP POSTERIOR PROBABILITY DISTRIBUTIONS P(C_k | X)       ")
    print("=" * 85)

    sample_test_rows = predictions.select("label", "prediction", "probability").limit(5).collect()
    for idx, row in enumerate(sample_test_rows, 1):
        actual = int(row["label"])
        pred = int(row["prediction"])
        probs = row["probability"].toArray()
        status = "✓ CORRECT" if actual == pred else "✗ MISCLASSIFIED"

        print(f"\n[Test Image {idx}] Actual Digit: {actual} | Predicted: {pred} ({status})")
        print("  Posterior Probabilities P(Digit = k | Image X):")
        for digit_k in range(10):
            bar = "█" * int(probs[digit_k] * 30)
            star = " <--- (ArgMax)" if digit_k == pred else ""
            print(f"    Digit {digit_k}: {probs[digit_k]:.6f} | {bar:<30}{star}")

    print("\n" + "=" * 85)
    spark.stop()


if __name__ == "__main__":
    main()
