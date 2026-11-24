#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 13: Bayes' Theorem for Two-Class Classification (Iris)
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v spark-submit >/dev/null 2>&1; then
    [ -x "/home/hp/spark/bin/spark-submit" ] && export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}" PATH="/home/hp/spark/bin:$PATH"
fi

DATASET="${1:-iris.csv}"
if [[ "$DATASET" != *"://"* ]] && [ -e "$DATASET" ]; then
    DATASET="file://$(realpath "$DATASET")"
fi

echo "========================================================================"
echo "  SUBMITTING QUESTION 13: BAYES' THEOREM (IRIS 2-CLASS) TO SPARK        "
echo "========================================================================"
spark-submit --master "local[*]" bayes_two_class.py "$DATASET"
