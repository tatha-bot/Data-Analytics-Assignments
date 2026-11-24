#!/usr/bin/env python3
"""Question 15: Compare Gaussian vs. Bernoulli Naive Bayes on Digit Images."""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, Binarizer, MinMaxScaler
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "digits_images.csv"
    spark = SparkSession.builder.appName("CompareGaussianBernoulliNB").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True).withColumn("label", col("label").cast("double"))
    pixel_cols = [c for c in df.columns if c.startswith("pixel_")]

    assembled = VectorAssembler(inputCols=pixel_cols, outputCol="raw_pixels").transform(df)
    scaled = MinMaxScaler(inputCol="raw_pixels", outputCol="features_cont").fit(assembled).transform(assembled)
    prepared = Binarizer(threshold=0.3, inputCol="features_cont", outputCol="features_bin").transform(scaled).cache()

    train_df, test_df = prepared.randomSplit([0.8, 0.2], seed=42)
    metrics = ("accuracy", "weightedPrecision", "weightedRecall", "f1")

    for model_type, feat_col in (("gaussian", "features_cont"), ("bernoulli", "features_bin")):
        t0 = time.time()
        model = NaiveBayes(featuresCol=feat_col, labelCol="label", modelType=model_type, smoothing=1.0).fit(train_df)
        elapsed = time.time() - t0
        preds = model.transform(test_df).cache()
        scores = {m: MulticlassClassificationEvaluator(metricName=m).evaluate(preds) for m in metrics}
        print(f"\n[{model_type.upper()} NB] Time={elapsed:.3f}s | " +
              " | ".join(f"{m}={scores[m]:.4f}" for m in metrics))
        if model_type == "bernoulli":
            preds.groupBy("label", "prediction").count().orderBy("label", "prediction").show(10)

    spark.stop()


if __name__ == "__main__":
    main()
