#!/usr/bin/env python3
"""
Question 15: Compare Gaussian and Bernoulli Naive Bayes on an Image Dataset
Big Data Analytics Lab Program

Compares two foundational Naive Bayes formulations on handwritten digit images (8x8 pixels):
  1. Gaussian Naive Bayes:
       - Models continuous grayscale pixel intensities using Gaussian Normal Distributions.
  2. Bernoulli Naive Bayes:
       - Binarizes pixel values (ink present vs. background) using Spark's Binarizer.
       - Models pixels as multivariate Bernoulli trials.

Metrics compared:
  - Training Time
  - Testing Accuracy
  - Weighted Precision & Recall
  - F1-Score
  - Per-class performance & Confusion Matrix
"""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, Binarizer, MinMaxScaler
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_images.csv"

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("CompareGaussianBernoulliNB") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 85)
    print("   BIG DATA ANALYTICS: GAUSSIAN VS. BERNOULLI NAIVE BAYES ON IMAGE DATASET   ")
    print("=" * 85)
    print(f"Loading image dataset from: {dataset_path}")

    # 2. Load Dataset
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]
    print(f"[+] Loaded {df.count()} handwritten digit images (8x8 = 64 pixels each, 10 classes 0-9).")

    # 3. Assemble continuous feature vector
    assembler = VectorAssembler(inputCols=pixel_cols, outputCol="raw_pixels")
    df_assembled = assembler.transform(df)

    # Scale pixel values to [0.0, 1.0]
    scaler = MinMaxScaler(inputCol="raw_pixels", outputCol="features_continuous")
    scaler_model = scaler.fit(df_assembled)
    df_continuous = scaler_model.transform(df_assembled)

    # Binarize pixel values for Bernoulli NB (threshold = 0.3: pixels > 0.3 become 1.0, else 0.0)
    binarizer = Binarizer(threshold=0.3, inputCol="features_continuous", outputCol="features_binary")
    df_prepared = binarizer.transform(df_continuous).cache()

    # Cast label to double
    df_prepared = df_prepared.withColumn("label", col("label").cast("double"))

    # 4. Train / Test Split (80% Train, 20% Test)
    train_df, test_df = df_prepared.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"[+] Train dataset: {train_count} images | Test dataset: {test_count} images")

    # Evaluators
    acc_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    prec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
    rec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")
    f1_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")

    # ==========================================================================
    # MODEL 1: GAUSSIAN NAIVE BAYES
    # ==========================================================================
    print("\n" + "-" * 85)
    print(">>> [1/2] Training Gaussian Naive Bayes (Continuous Pixel Intensities)...")
    print("-" * 85)
    t0 = time.time()
    nb_gaussian = NaiveBayes(featuresCol="features_continuous", labelCol="label", modelType="gaussian")
    model_gaussian = nb_gaussian.fit(train_df)
    train_time_g = time.time() - t0

    t0 = time.time()
    preds_gaussian = model_gaussian.transform(test_df).cache()
    infer_time_g = time.time() - t0

    acc_g = acc_eval.evaluate(preds_gaussian)
    prec_g = prec_eval.evaluate(preds_gaussian)
    rec_g = rec_eval.evaluate(preds_gaussian)
    f1_g = f1_eval.evaluate(preds_gaussian)

    print(f"  • Training Time  : {train_time_g:.3f} s")
    print(f"  • Test Accuracy  : {acc_g * 100:.2f}%")
    print(f"  • Precision      : {prec_g * 100:.2f}%")
    print(f"  • Recall         : {rec_g * 100:.2f}%")
    print(f"  • F1-Score       : {f1_g:.4f}")

    # ==========================================================================
    # MODEL 2: BERNOULLI NAIVE BAYES
    # ==========================================================================
    print("\n" + "-" * 85)
    print(">>> [2/2] Training Bernoulli Naive Bayes (Binarized Binary Pixels)...")
    print("-" * 85)
    t0 = time.time()
    nb_bernoulli = NaiveBayes(featuresCol="features_binary", labelCol="label", modelType="bernoulli", smoothing=1.0)
    model_bernoulli = nb_bernoulli.fit(train_df)
    train_time_b = time.time() - t0

    t0 = time.time()
    preds_bernoulli = model_bernoulli.transform(test_df).cache()
    infer_time_b = time.time() - t0

    acc_b = acc_eval.evaluate(preds_bernoulli)
    prec_b = prec_eval.evaluate(preds_bernoulli)
    rec_b = rec_eval.evaluate(preds_bernoulli)
    f1_b = f1_eval.evaluate(preds_bernoulli)

    print(f"  • Training Time  : {train_time_b:.3f} s")
    print(f"  • Test Accuracy  : {acc_b * 100:.2f}%")
    print(f"  • Precision      : {prec_b * 100:.2f}%")
    print(f"  • Recall         : {rec_b * 100:.2f}%")
    print(f"  • F1-Score       : {f1_b:.4f}")

    # ==========================================================================
    # COMPARATIVE SUMMARY TABLE
    # ==========================================================================
    print("\n" + "=" * 85)
    print("        COMPREHENSIVE PERFORMANCE COMPARISON: GAUSSIAN VS. BERNOULLI NAIVE BAYES       ")
    print("=" * 85)
    print(f"{'Metric':<25} | {'Gaussian Naive Bayes':<25} | {'Bernoulli Naive Bayes':<25}")
    print("-" * 85)
    print(f"{'Feature Type':<25} | {'Continuous [0.0 - 1.0]':<25} | {'Binary {0.0, 1.0}':<25}")
    print(f"{'Training Time (s)':<25} | {train_time_g:<25.4f} | {train_time_b:<25.4f}")
    print(f"{'Accuracy (%)':<25} | {acc_g * 100:<25.2f} | {acc_b * 100:<25.2f}")
    print(f"{'Weighted Precision (%)':<25} | {prec_g * 100:<25.2f} | {prec_b * 100:<25.2f}")
    print(f"{'Weighted Recall (%)':<25} | {rec_g * 100:<25.2f} | {rec_b * 100:<25.2f}")
    print(f"{'F1-Score':<25} | {f1_g:<25.4f} | {f1_b:<25.4f}")
    print("=" * 85)

    # 5. Theoretical Comparison & Analytical Conclusions
    print("\n--- Analytical Insights ---")
    if acc_b >= acc_g:
        print("  ✓ Bernoulli Naive Bayes achieves superior or competitive accuracy on handwritten digit images.")
        print("    Reason: For digit images, whether a pixel is inked (1) or blank (0) carries strong shape signal.")
        print("    Gaussian NB assumes normal bell-curve pixel variance, whereas digit pixels are bi-modal (either black or white).")
    else:
        print("  ✓ Gaussian Naive Bayes achieves superior accuracy on this representation.")
        print("    Reason: Continuous stroke intensity gradients preserve pen pressure nuances.")

    print("\n--- Confusion Matrix Sample (Bernoulli NB) ---")
    preds_bernoulli.groupBy("label", "prediction").count().orderBy("label", "prediction").show(10)

    spark.stop()


if __name__ == "__main__":
    main()
