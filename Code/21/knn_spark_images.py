#!/usr/bin/env python3
"""Question 21: Distributed K-NN Image Classification on Apache Spark (RDD + Broadcast)."""

import sys
from collections import Counter
import numpy as np
from pyspark.sql import SparkSession


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_knn.csv"
    k_val = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    spark = SparkSession.builder.appName("DistributedKNNImages").master("local[*]").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    to_vec = lambda rows: [
        (int(r["label"]), np.array([float(r[c]) / 16.0 for c in pixel_cols], dtype=np.float32))
        for r in rows
    ]
    train_bc = sc.broadcast(to_vec(train_df.collect()))
    test_rdd = sc.parallelize(to_vec(test_df.collect()), numSlices=4).cache()
    test_n = test_rdd.count()

    def predict_partition(part, k):
        train_local = train_bc.value
        for actual, q in part:
            dists = sorted((float(np.linalg.norm(q - tr)), lbl) for lbl, tr in train_local)
            pred = Counter(lbl for _, lbl in dists[:k]).most_common(1)[0][0]
            yield (actual, pred, dists[0][0])

    preds = test_rdd.mapPartitions(lambda p: predict_partition(p, k_val)).collect()
    acc = sum(a == p for a, p, _ in preds) / test_n * 100
    print(f"[Distributed K-NN (k={k_val})] Accuracy: {acc:.2f}% ({sum(a == p for a, p, _ in preds)}/{test_n})")

    print("\n=== K Hyperparameter Sweep ===")
    best_k, best_acc = k_val, acc
    for k in (1, 3, 5, 7, 9):
        k_preds = test_rdd.mapPartitions(lambda p: predict_partition(p, k)).collect()
        k_acc = sum(a == p for a, p, _ in k_preds) / test_n * 100
        print(f"  k={k}: {k_acc:.2f}%")
        if k_acc > best_acc:
            best_k, best_acc = k, k_acc
    print(f"Best k = {best_k} ({best_acc:.2f}%)")

    conf = np.zeros((10, 10), dtype=int)
    for a, p, _ in preds:
        conf[a, p] += 1
    print("\n=== 10x10 Confusion Matrix ===\n" + str(conf))

    spark.stop()


if __name__ == "__main__":
    main()
