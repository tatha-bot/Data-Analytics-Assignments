#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 7: Clustering Techniques using Spark
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v spark-submit >/dev/null 2>&1; then
    [ -x "/home/hp/spark/bin/spark-submit" ] && export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}" PATH="/home/hp/spark/bin:$PATH"
fi

DATASET="${1:-clustering_data.csv}"
if [[ "$DATASET" != *"://"* ]] && [ -e "$DATASET" ]; then
    DATASET="file://$(realpath "$DATASET")"
fi

echo "========================================================================"
echo "  SUBMITTING QUESTION 7: CLUSTERING TECHNIQUES TO APACHE SPARK          "
echo "========================================================================"
spark-submit --master "local[*]" clustering_spark.py "$DATASET"
