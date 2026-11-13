#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 21: Distributed K-NN Image Classification on Spark
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-digits_knn.csv}"
K_VAL="${2:-3}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 21: DISTRIBUTED K-NN (HANDWRITTEN DIGITS) TO SPARK"
echo "========================================================================"
spark-submit --master "local[*]" knn_spark_images.py "$DATASET" "$K_VAL"
