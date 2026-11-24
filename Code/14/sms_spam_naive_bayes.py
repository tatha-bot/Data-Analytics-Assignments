#!/usr/bin/env python3
"""Question 14: SMS Spam Detection using Spark NLP Pipeline & Multinomial Naive Bayes."""

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "spam.csv"
    spark = SparkSession.builder.appName("SMSSpamNaiveBayes").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.csv(dataset_path, header=True, inferSchema=True) \
        .filter(col("message").isNotNull() & col("label").isNotNull())
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    pipeline = Pipeline(stages=[
        StringIndexer(inputCol="label", outputCol="label_index"),
        RegexTokenizer(inputCol="message", outputCol="tokens", pattern=r"\W+", toLowercase=True),
        StopWordsRemover(inputCol="tokens", outputCol="filtered"),
        HashingTF(inputCol="filtered", outputCol="raw_features", numFeatures=4096),
        IDF(inputCol="raw_features", outputCol="features"),
        NaiveBayes(featuresCol="features", labelCol="label_index", modelType="multinomial", smoothing=1.0),
    ])

    model = pipeline.fit(train_df)
    preds = model.transform(test_df).cache()

    print("=== SMS Spam Naive Bayes Evaluation ===")
    for m in ("accuracy", "weightedPrecision", "weightedRecall", "f1"):
        val = MulticlassClassificationEvaluator(labelCol="label_index", metricName=m).evaluate(preds)
        print(f"  {m}: {val:.4f}")
    preds.groupBy("label", "prediction").count().orderBy("label").show()

    samples = [
        ("Hey bro, are we going to the library today?",),
        ("CONGRATULATIONS! You won a $1,000 cash prize. Call 0800123456 NOW!",),
        ("URGENT: Your bank account is suspended. Verify at http://bit.ly/login",),
    ]
    labels = ["ham", "spam"]
    sample_preds = model.transform(spark.createDataFrame(samples, ["message"])).collect()
    for r in sample_preds:
        print(f"[{labels[int(r['prediction'])].upper()}] {r['message']}")

    spark.stop()


if __name__ == "__main__":
    main()
