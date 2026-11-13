#!/usr/bin/env python3
"""
Question 7: Implement Clustering Techniques using Apache Spark MLlib
Big Data Analytics Lab Program

Demonstrates three major distributed clustering techniques:
  1. K-Means Clustering (pyspark.ml.clustering.KMeans)
  2. Bisecting K-Means Clustering (pyspark.ml.clustering.BisectingKMeans - Hierarchical Divisive)
  3. Gaussian Mixture Models (pyspark.ml.clustering.GaussianMixture - Probabilistic Soft Clustering)

Also performs:
  - Feature scaling with StandardScaler
  - Clustering quality evaluation using ClusteringEvaluator (Silhouette Score)
  - Optimal k exploration using Silhouette analysis across k = 2 to 6
"""

import sys
import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans, BisectingKMeans, GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "clustering_data.csv"

    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("ClusteringTechniquesSpark") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=" * 80)
    print("       BIG DATA ANALYTICS: CLUSTERING TECHNIQUES USING APACHE SPARK       ")
    print("=" * 80)
    print(f"Loading dataset from: {dataset_path}")

    # 2. Load Dataset into Spark DataFrame
    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    print(f"\n[+] Loaded Dataset with {df.count()} records and {len(df.columns)} columns.")
    print("\n--- Schema ---")
    df.printSchema()

    print("\n--- Sample Data Preview (First 5 Rows) ---")
    df.show(5, truncate=False)

    # 3. Feature Assembly and Scaling
    feature_cols = [c for c in df.columns if c.lower() not in ["customerid", "id", "label", "cluster"]]
    print(f"[+] Feature columns used for clustering: {feature_cols}")

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
    df_assembled = assembler.transform(df)

    scaler = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=False)
    scaler_model = scaler.fit(df_assembled)
    data = scaler_model.transform(df_assembled).cache()

    evaluator = ClusteringEvaluator(featuresCol="features",
                                    predictionCol="prediction",
                                    metricName="silhouette",
                                    distanceMeasure="squaredEuclidean")

    k_clusters = 3
    print("\n" + "=" * 80)
    print(f"   COMPARING 3 CLUSTERING ALGORITHMS ON SPARK WITH k = {k_clusters}   ")
    print("=" * 80)

    results = []

    # --------------------------------------------------------------------------
    # TECHNIQUE 1: K-Means Clustering
    # --------------------------------------------------------------------------
    print("\n>>> [1/3] Running Standard K-Means Clustering...")
    t0 = time.time()
    kmeans = KMeans(k=k_clusters, seed=42, featuresCol="features", predictionCol="prediction")
    km_model = kmeans.fit(data)
    km_preds = km_model.transform(data)
    km_sil = evaluator.evaluate(km_preds)
    km_time = time.time() - t0

    results.append(("K-Means", km_sil, km_time))
    print(f"    - Silhouette Score : {km_sil:.4f}")
    print(f"    - Training Time    : {km_time:.2f} seconds")
    print("    - Cluster Centers (Standardized Space):")
    for idx, center in enumerate(km_model.clusterCenters()):
        center_str = ", ".join([f"{val:.2f}" for val in center[:4]])
        print(f"        Cluster {idx}: [{center_str}, ...]")

    print("    - Points per cluster:")
    km_preds.groupBy("prediction").count().orderBy("prediction").show()

    # --------------------------------------------------------------------------
    # TECHNIQUE 2: Bisecting K-Means Clustering (Divisive Hierarchical)
    # --------------------------------------------------------------------------
    print("\n>>> [2/3] Running Bisecting K-Means Clustering...")
    t0 = time.time()
    bkm = BisectingKMeans(k=k_clusters, seed=42, featuresCol="features", predictionCol="prediction")
    bkm_model = bkm.fit(data)
    bkm_preds = bkm_model.transform(data)
    bkm_sil = evaluator.evaluate(bkm_preds)
    bkm_time = time.time() - t0

    results.append(("Bisecting K-Means", bkm_sil, bkm_time))
    print(f"    - Silhouette Score : {bkm_sil:.4f}")
    print(f"    - Training Time    : {bkm_time:.2f} seconds")
    print("    - Cluster Centers:")
    for idx, center in enumerate(bkm_model.clusterCenters()):
        center_str = ", ".join([f"{val:.2f}" for val in center[:4]])
        print(f"        Cluster {idx}: [{center_str}, ...]")

    print("    - Points per cluster:")
    bkm_preds.groupBy("prediction").count().orderBy("prediction").show()

    # --------------------------------------------------------------------------
    # TECHNIQUE 3: Gaussian Mixture Model (GMM - Probabilistic Soft Clustering)
    # --------------------------------------------------------------------------
    print("\n>>> [3/3] Running Gaussian Mixture Model (GMM)...")
    t0 = time.time()
    gmm = GaussianMixture(k=k_clusters, seed=42, featuresCol="features", predictionCol="prediction")
    gmm_model = gmm.fit(data)
    gmm_preds = gmm_model.transform(data)
    gmm_sil = evaluator.evaluate(gmm_preds)
    gmm_time = time.time() - t0

    results.append(("Gaussian Mixture (GMM)", gmm_sil, gmm_time))
    print(f"    - Silhouette Score : {gmm_sil:.4f}")
    print(f"    - Training Time    : {gmm_time:.2f} seconds")
    print("    - Component Weights:")
    for idx, weight in enumerate(gmm_model.weights):
        print(f"        Component {idx}: Weight = {weight:.4f}")

    print("    - Points per cluster (Hard Assignment via argmax probability):")
    gmm_preds.groupBy("prediction").count().orderBy("prediction").show()

    # --------------------------------------------------------------------------
    # COMPARISON SUMMARY
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("               CLUSTERING TECHNIQUES PERFORMANCE SUMMARY               ")
    print("=" * 80)
    print(f"{'Algorithm':<25} | {'Silhouette Score':<20} | {'Training Time (s)':<18}")
    print("-" * 80)
    for name, sil, runtime in results:
        print(f"{name:<25} | {sil:<20.4f} | {runtime:<18.2f}")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # OPTIMAL K EXPLORATION (Elbow / Silhouette Scan across k = 2 to 5)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("       OPTIMAL k EXPLORATION VIA SILHOUETTE ANALYSIS (K-MEANS)       ")
    print("=" * 80)
    print(f"{'k (Number of Clusters)':<25} | {'Silhouette Score':<20}")
    print("-" * 50)
    best_k = 2
    best_score = -1.0
    for k_val in range(2, 6):
        km = KMeans(k=k_val, seed=42, featuresCol="features", predictionCol="prediction")
        km_m = km.fit(data)
        preds = km_m.transform(data)
        score = evaluator.evaluate(preds)
        print(f"{k_val:<25} | {score:<20.4f}")
        if score > best_score:
            best_score = score
            best_k = k_val
    print("-" * 50)
    print(f"[+] Optimal k based on maximum Silhouette Score: k = {best_k} (Score: {best_score:.4f})")
    print("=" * 80)

    spark.stop()


if __name__ == "__main__":
    main()
