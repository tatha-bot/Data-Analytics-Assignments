#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 21: Distributed K-NN Image Classification on Spark
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v spark-submit >/dev/null 2>&1; then
    [ -x "/home/hp/spark/bin/spark-submit" ] && export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}" PATH="/home/hp/spark/bin:$PATH"
fi

DATASET="${1:-digits_knn.csv}"
if [[ "$DATASET" != *"://"* ]] && [ -e "$DATASET" ]; then
    DATASET="file://$(realpath "$DATASET")"
fi
K_VAL="${2:-3}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 21: DISTRIBUTED K-NN (HANDWRITTEN DIGITS) TO SPARK"
echo "========================================================================"
spark-submit --master "local[*]" knn_spark_images.py "$DATASET" "$K_VAL"
