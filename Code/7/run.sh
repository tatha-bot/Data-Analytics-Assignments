#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 7: Clustering Techniques using Spark
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-clustering_data.csv}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 7: CLUSTERING TECHNIQUES TO APACHE SPARK          "
echo "========================================================================"
spark-submit --master "local[*]" clustering_spark.py "$DATASET"
