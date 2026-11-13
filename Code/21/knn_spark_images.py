#!/usr/bin/env python3
"""
Question 21: Apply K-Nearest Neighbour (K-NN) Algorithm for Classification of Handwritten Image Dataset
Big Data Analytics Lab Program

Demonstrates:
  1. Distributed Big Data K-NN using Apache Spark RDD and Broadcast variables:
       - Distance Metric: Euclidean Distance ||X_q - X_i||_2 in 64-dimensional pixel space
       - Parallel Query Execution: Query instances are partitioned across Spark workers
       - Parallel neighbor extraction & Majority Voting via collections.Counter
  2. Hyperparameter Exploration:
       - Compares K = 1, 3, 5, 7 to find optimal K
  3. Comprehensive Evaluation:
       - Classification Accuracy, Confusion Matrix, Precision, Recall
       - Sample Predictions preview with distance to closest neighbor
"""

import sys
import time
import math
from collections import Counter
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import numpy as np


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_knn.csv"
    k_neighbors = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("DistributedKNNImages") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    print("=" * 85)
    print("    BIG DATA ANALYTICS: DISTRIBUTED K-NEAREST NEIGHBOURS (K-NN) ON SPARK    ")
    print("=" * 85)
    print(f"Loading handwritten image dataset from: {dataset_path}")

    # 2. Load dataset
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]

    total_images = df.count()
    print(f"[+] Loaded {total_images} images (8x8 = 64 pixel features each, classes 0-9).")

    # 3. Train / Test Split (80% Train, 20% Test)
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"[+] Training Set : {train_count} images")
    print(f"[+] Testing Set  : {test_count} images")

    # Convert to lightweight records: (label, [pixel_values normalized to 0.0-1.0])
    train_rows = train_df.collect()
    test_rows = test_df.collect()

    train_data = [(int(r["label"]), np.array([float(r[col_name]) / 16.0 for col_name in pixel_cols], dtype=np.float32))
                  for r in train_rows]
    test_data = [(int(r["label"]), np.array([float(r[col_name]) / 16.0 for col_name in pixel_cols], dtype=np.float32))
                 for r in test_rows]

    # 4. Broadcast training dataset to all Spark executor nodes
    print("\n[+] Broadcasting training set to Spark executors for distributed distance computation...")
    train_broadcast = sc.broadcast(train_data)

    # 5. Define Distributed KNN Prediction Function
    def predict_partition(test_partition, k_val):
        """Processes a partition of query images in parallel on executor."""
        local_train = train_broadcast.value
        partition_results = []

        for actual_label, query_vec in test_partition:
            # Vectorized Euclidean distance calculation against all training images
            distances = []
            for tr_label, tr_vec in local_train:
                # Euclidean distance: ||query_vec - tr_vec||
                dist = float(np.linalg.norm(query_vec - tr_vec))
                distances.append((dist, tr_label))

            # Partial sort to extract top k smallest distances
            distances.sort(key=lambda item: item[0])
            top_k = distances[:k_val]

            # Majority voting
            top_labels = [label for _, label in top_k]
            predicted_label = Counter(top_labels).most_common(1)[0][0]
            closest_dist = top_k[0][0]

            partition_results.append((actual_label, predicted_label, closest_dist))

        return partition_results

    # 6. Evaluate K-NN for Selected K
    print("\n" + "=" * 85)
    print(f"               RUNNING DISTRIBUTED K-NN PREDICTION (k = {k_neighbors})              ")
    print("=" * 85)

    test_rdd = sc.parallelize(test_data, numSlices=4)

    t0 = time.time()
    predictions = test_rdd.mapPartitions(lambda part: predict_partition(part, k_neighbors)).collect()
    inference_time = time.time() - t0

    # Calculate Accuracy
    correct = sum(1 for actual, pred, _ in predictions if actual == pred)
    accuracy = correct / float(test_count)

    print(f"  • Total Test Images Evaluated : {test_count}")
    print(f"  • Correctly Classified        : {correct}")
    print(f"  • Misclassified               : {test_count - correct}")
    print(f"  • Classification Accuracy     : {accuracy * 100:.2f}%")
    print(f"  • Total Parallel Time         : {inference_time:.2f} seconds")
    print(f"  • Average Latency per Image   : {(inference_time / test_count) * 1000:.2f} ms")
    print("=" * 85)

    # 7. Sample Predictions Preview
    print("\n--- Sample Test Image Predictions (First 10) ---")
    print(f"{'Index':<8} | {'Actual':<8} | {'Predicted':<10} | {'Distance to Nearest':<22} | {'Result'}")
    print("-" * 65)
    for idx, (actual, pred, nearest_dist) in enumerate(predictions[:10], 1):
        status = "✓ CORRECT" if actual == pred else "✗ MISMATCH"
        print(f"{idx:<8} | {actual:<8} | {pred:<10} | {nearest_dist:<22.4f} | {status}")

    # 8. Hyperparameter Search across multiple values of K
    print("\n" + "=" * 85)
    print("          K-NN HYPERPARAMETER ANALYSIS: EXPLORING DIFFERENT VALUES OF K        ")
    print("=" * 85)
    print(f"{'K Value':<15} | {'Accuracy (%)':<20} | {'Correct / Total':<20} | {'Latency (s)':<15}")
    print("-" * 80)

    best_k = k_neighbors
    best_acc = accuracy

    for test_k in [1, 3, 5, 7, 9]:
        t_start = time.time()
        k_preds = test_rdd.mapPartitions(lambda part: predict_partition(part, test_k)).collect()
        t_dur = time.time() - t_start
        k_correct = sum(1 for actual, pred, _ in k_preds if actual == pred)
        k_acc = (k_correct / float(test_count)) * 100
        print(f"k = {test_k:<11} | {k_acc:<20.2f} | {k_correct}/{test_count:<18} | {t_dur:<15.2f}")
        if k_acc > best_acc:
            best_acc = k_acc
            best_k = test_k

    print("-" * 80)
    print(f"[+] Optimal Hyperparameter: k = {best_k} (Accuracy = {best_acc:.2f}%)")
    print("=" * 85)

    # 9. Confusion Matrix for best K
    print("\n--- 10-Class Confusion Matrix ---")
    conf_matrix = np.zeros((10, 10), dtype=int)
    for actual, pred, _ in predictions:
        conf_matrix[actual, pred] += 1

    header = "Actual \\ Pred | " + " ".join([f"{i:>4}" for i in range(10)])
    print(header)
    print("-" * len(header))
    for i in range(10):
        row_str = f"Digit {i:>2}       | " + " ".join([f"{conf_matrix[i, j]:>4}" for j in range(10)])
        print(row_str)

    spark.stop()


if __name__ == "__main__":
    main()
