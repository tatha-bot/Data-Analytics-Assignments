#!/usr/bin/env python3
"""Question 7: Clustering Techniques (K-Means, Bisecting K-Means, GMM) on Apache Spark."""

import sys
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans, BisectingKMeans, GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "clustering_data.csv"
    spark = SparkSession.builder.appName("ClusteringSpark").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True)
    feature_cols = [c for c in df.columns if c.lower() not in ("customerid", "id", "label", "cluster")]

    assembled = VectorAssembler(inputCols=feature_cols, outputCol="raw_features").transform(df)
    data = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=False) \
        .fit(assembled).transform(assembled).cache()

    evaluator = ClusteringEvaluator(metricName="silhouette", distanceMeasure="squaredEuclidean")
    models = [
        ("K-Means", KMeans(k=3, seed=42)),
        ("Bisecting K-Means", BisectingKMeans(k=3, seed=42)),
        ("Gaussian Mixture", GaussianMixture(k=3, seed=42)),
    ]

    print("=== Clustering Comparison (k=3) ===")
    for name, algo in models:
        preds = algo.fit(data).transform(data)
        score = evaluator.evaluate(preds)
        print(f"\n[{name}] Silhouette Score: {score:.4f}")
        preds.groupBy("prediction").count().orderBy("prediction").show()

    print("=== Optimal k Exploration (K-Means) ===")
    scores = {k: evaluator.evaluate(KMeans(k=k, seed=42).fit(data).transform(data)) for k in range(2, 6)}
    for k, s in scores.items():
        print(f"k={k}: Silhouette = {s:.4f}")
    best_k = max(scores, key=scores.get)
    print(f"Optimal k = {best_k} (Score: {scores[best_k]:.4f})")

    spark.stop()


if __name__ == "__main__":
    main()
