#!/usr/bin/env python3
"""Question 13: Two-Class Bayes' Theorem (First-Principles Spark + MLlib) on Iris."""

import sys
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, stddev_pop
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def gaussian_pdf(x, mu, sigma):
    sigma = sigma if sigma and sigma > 0 else 1e-4
    return (1.0 / (math.sqrt(2 * math.pi) * sigma)) * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "iris.csv"
    spark = SparkSession.builder.appName("BayesTwoClassIris").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True) \
        .filter(col("species").isin(["setosa", "versicolor"]))
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    train_n, test_n = train_df.count(), test_df.count()
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    # Part 1: First-Principles Bayes' Theorem via Spark Aggregations
    priors = {r["species"]: r["count"] / train_n for r in train_df.groupBy("species").count().collect()}
    aggs = [fn(col(f)).alias(f"{f}_{tag}") for f in features for fn, tag in ((avg, "mu"), (stddev_pop, "sd"))]
    stats = {
        r["species"]: {f: (r[f"{f}_mu"], r[f"{f}_sd"]) for f in features}
        for r in train_df.groupBy("species").agg(*aggs).collect()
    }

    correct = 0
    for r in test_df.collect():
        post = {}
        for cls, prior in priors.items():
            lik = math.prod(gaussian_pdf(float(r[f]), *stats[cls][f]) for f in features)
            post[cls] = prior * lik
        pred = max(post, key=post.get)
        correct += int(pred == r["species"])
    print(f"[Part 1: First-Principles Bayes] Accuracy: {correct / test_n * 100:.2f}% ({correct}/{test_n})")

    # Part 2: Spark MLlib Gaussian Naive Bayes
    idx_model = StringIndexer(inputCol="species", outputCol="label").fit(train_df)
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    train_ml = assembler.transform(idx_model.transform(train_df))
    test_ml = assembler.transform(idx_model.transform(test_df))

    preds = NaiveBayes(modelType="gaussian").fit(train_ml).transform(test_ml)
    print("\n[Part 2: Spark MLlib NaiveBayes(gaussian)]")
    for m in ("accuracy", "weightedPrecision", "weightedRecall", "f1"):
        val = MulticlassClassificationEvaluator(metricName=m).evaluate(preds)
        print(f"  {m}: {val:.4f}")
    preds.groupBy("species", "prediction").count().show()

    spark.stop()


if __name__ == "__main__":
    main()
