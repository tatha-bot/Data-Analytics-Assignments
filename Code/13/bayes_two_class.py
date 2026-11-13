#!/usr/bin/env python3
"""
Question 13: Implement Bayes' Theorem for Two-Class Classification using Iris Dataset
Big Data Analytics Lab Program

Demonstrates:
  1. Distributed Mathematical Bayes' Theorem from first principles using Spark DataFrame aggregations:
       - Prior: P(C_k)
       - Feature likelihood: Gaussian PDF P(x_j | C_k) with distributed mean and variance
       - Posterior: P(C_k | X) = [P(C_k) * prod P(x_j | C_k)] / P(X)
  2. Apache Spark MLlib Pipeline implementation:
       - VectorAssembler + NaiveBayes(modelType="gaussian")
  3. Evaluation: Accuracy, Precision, Recall, Confusion Matrix
"""

import sys
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, stddev_pop, when, lit
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "iris.csv"

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("BayesTwoClassIris") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 80)
    print("   BIG DATA ANALYTICS: BAYES' THEOREM FOR 2-CLASS CLASSIFICATION (IRIS)   ")
    print("=" * 80)
    print(f"Loading Iris dataset from: {dataset_path}")

    # 2. Load dataset
    raw_df = spark.read.csv(dataset_path, header=True, inferSchema=True)

    # Filter to two distinct classes: setosa vs versicolor
    df_two_class = raw_df.filter(col("species").isin(["setosa", "versicolor"]))
    print(f"[+] Total records for 2-class subset (setosa & versicolor): {df_two_class.count()}")
    df_two_class.groupBy("species").count().show()

    # 3. Train / Test Split (80% Train, 20% Test)
    train_df, test_df = df_two_class.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"[+] Train split: {train_count} records | Test split: {test_count} records")

    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    # ==========================================================================
    # PART 1: FIRST-PRINCIPLES BAYES' THEOREM USING SPARK DISTRIBUTED AGGREGATIONS
    # ==========================================================================
    print("\n" + "=" * 80)
    print("  PART 1: MATHEMATICAL BAYES' THEOREM FROM DISTRIBUTED SPARK AGGREGATIONS  ")
    print("=" * 80)

    # Compute Class Priors P(C)
    priors_df = train_df.groupBy("species").count()
    priors = {row["species"]: row["count"] / float(train_count) for row in priors_df.collect()}
    print("\n--- 1. Class Priors P(C) ---")
    for cls, pr in priors.items():
        print(f"    P(Species = '{cls}') = {pr:.4f}")

    # Compute Feature Mean and Variance per Class using Spark aggregations
    agg_exprs = []
    for f in features:
        agg_exprs.append(avg(col(f)).alias(f"{f}_mean"))
        agg_exprs.append(stddev_pop(col(f)).alias(f"{f}_std"))

    stats_df = train_df.groupBy("species").agg(*agg_exprs)
    print("\n--- 2. Learned Gaussian Parameters (Mean and Std Dev) per Class ---")
    stats_df.show(truncate=False)

    stats_map = {}
    for row in stats_df.collect():
        cls = row["species"]
        stats_map[cls] = {}
        for f in features:
            mu = row[f"{f}_mean"]
            std = row[f"{f}_std"]
            # Avoid division by zero
            if std == 0.0 or std is None:
                std = 1e-4
            stats_map[cls][f] = (mu, std)

    # Gaussian PDF Likelihood function: P(x | mu, sigma)
    def gaussian_pdf(x, mu, sigma):
        exponent = math.exp(-((x - mu) ** 2) / (2 * (sigma ** 2)))
        return (1.0 / (math.sqrt(2 * math.pi) * sigma)) * exponent

    # Perform Bayes' Rule prediction on Test Set
    print("--- 3. Evaluating Bayes' Theorem on Unseen Test Set ---")
    test_rows = test_df.collect()
    fp_predictions = []

    print(f"{'Actual':<12} | {'P(setosa|X)':<15} | {'P(versicolor|X)':<15} | {'Predicted':<12} | {'Match?'}")
    print("-" * 65)

    correct_math = 0
    for r in test_rows:
        actual = r["species"]
        # Likelihood * Prior for each class
        posteriors = {}
        for cls in ["setosa", "versicolor"]:
            prior = priors[cls]
            likelihood = 1.0
            for f in features:
                val = float(r[f])
                mu, std = stats_map[cls][f]
                likelihood *= gaussian_pdf(val, mu, std)
            posteriors[cls] = prior * likelihood

        # Normalize posteriors: P(C | X) = Likelihood*Prior / sum
        evidence = sum(posteriors.values())
        norm_posteriors = {cls: (posteriors[cls] / evidence) if evidence > 0 else 0.5 for cls in posteriors}

        pred = max(norm_posteriors, key=norm_posteriors.get)
        matched = "✓" if pred == actual else "✗"
        if pred == actual:
            correct_math += 1

        print(f"{actual:<12} | {norm_posteriors['setosa']:<15.6f} | {norm_posteriors['versicolor']:<15.6f} | {pred:<12} | {matched}")

    acc_math = correct_math / float(test_count)
    print("-" * 65)
    print(f"[+] Mathematical Bayes' Theorem Test Accuracy: {acc_math * 100:.2f}% ({correct_math}/{test_count})")

    # ==========================================================================
    # PART 2: APACHE SPARK MLlib NAIVE BAYES PIPELINE
    # ==========================================================================
    print("\n" + "=" * 80)
    print("      PART 2: APACHE SPARK MLlib NaiveBayes(modelType='gaussian')        ")
    print("=" * 80)

    # StringIndexer for species label
    indexer = StringIndexer(inputCol="species", outputCol="label")
    indexer_model = indexer.fit(train_df)
    train_indexed = indexer_model.transform(train_df)
    test_indexed = indexer_model.transform(test_df)

    # VectorAssembler for features
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    train_assembled = assembler.transform(train_indexed)
    test_assembled = assembler.transform(test_indexed)

    # Train Gaussian Naive Bayes Model
    nb = NaiveBayes(modelType="gaussian", featuresCol="features", labelCol="label")
    nb_model = nb.fit(train_assembled)

    # Predict on test set
    predictions = nb_model.transform(test_assembled)

    print("\n--- Spark MLlib Predictions (Sample) ---")
    predictions.select("species", "features", "probability", "prediction", "label").show(5, truncate=False)

    # Evaluators
    acc_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    f1_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
    prec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
    rec_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")

    accuracy = acc_eval.evaluate(predictions)
    f1 = f1_eval.evaluate(predictions)
    precision = prec_eval.evaluate(predictions)
    recall = rec_eval.evaluate(predictions)

    print("=" * 80)
    print("                SPARK MLlib NAIVE BAYES EVALUATION SUMMARY              ")
    print("=" * 80)
    print(f"  • Accuracy           : {accuracy * 100:.2f}%")
    print(f"  • Weighted Precision : {precision * 100:.2f}%")
    print(f"  • Weighted Recall    : {recall * 100:.2f}%")
    print(f"  • F1-Score           : {f1:.4f}")
    print("=" * 80)

    # Confusion Matrix
    print("\n--- Confusion Matrix ---")
    predictions.groupBy("species", "prediction").count().show()

    spark.stop()


if __name__ == "__main__":
    main()
