#!/usr/bin/env python3
"""Question 16: Multiclass Bayes' Theorem Classification on Digit Images."""

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_multiclass.csv"
    spark = SparkSession.builder.appName("BayesMulticlassImages").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True).withColumn("label", col("label").cast("double"))
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]

    assembled = VectorAssembler(inputCols=pixel_cols, outputCol="raw_features").transform(df)
    scaled = MinMaxScaler(inputCol="raw_features", outputCol="features").fit(assembled).transform(assembled).cache()
    train_df, test_df = scaled.randomSplit([0.8, 0.2], seed=42)
    train_n = train_df.count()

    print("=== Class Priors P(C_k) ===")
    for r in train_df.groupBy("label").count().orderBy("label").collect():
        print(f"  Digit {int(r['label'])}: {r['count'] / train_n:.4f}")

    preds = NaiveBayes(modelType="multinomial", smoothing=1.0).fit(train_df).transform(test_df).cache()

    print("\n=== Multiclass Evaluation ===")
    for m in ("accuracy", "weightedPrecision", "weightedRecall", "f1"):
        print(f"  {m}: {MulticlassClassificationEvaluator(metricName=m).evaluate(preds):.4f}")

    print("\n=== 10x10 Confusion Matrix ===")
    preds.crosstab("label", "prediction").orderBy("label_prediction").show(10, truncate=False)

    print("=== Sample Posterior Probabilities ===")
    for i, r in enumerate(preds.select("label", "prediction", "probability").limit(3).collect(), 1):
        probs = [f"{k}:{p:.2f}" for k, p in enumerate(r["probability"].toArray()) if p >= 0.01]
        print(f"  Sample {i}: actual={int(r['label'])}, pred={int(r['prediction'])} | {', '.join(probs)}")

    spark.stop()


if __name__ == "__main__":
    main()
