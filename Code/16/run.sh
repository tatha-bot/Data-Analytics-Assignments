#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 16: Bayes' Theorem for Multiclass Image Classification
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v spark-submit >/dev/null 2>&1; then
    [ -x "/home/hp/spark/bin/spark-submit" ] && export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}" PATH="/home/hp/spark/bin:$PATH"
fi

DATASET="${1:-digits_multiclass.csv}"
if [[ "$DATASET" != *"://"* ]] && [ -e "$DATASET" ]; then
    DATASET="file://$(realpath "$DATASET")"
fi

echo "========================================================================"
echo "  SUBMITTING QUESTION 16: MULTICLASS BAYES' THEOREM (DIGITS) TO SPARK   "
echo "========================================================================"
spark-submit --master "local[*]" bayes_multiclass_images.py "$DATASET"
