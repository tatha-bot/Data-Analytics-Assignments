#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 14: SMS Spam Detection via Spark Naive Bayes
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v spark-submit >/dev/null 2>&1; then
    [ -x "/home/hp/spark/bin/spark-submit" ] && export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}" PATH="/home/hp/spark/bin:$PATH"
fi

DATASET="${1:-spam.csv}"
if [[ "$DATASET" != *"://"* ]] && [ -e "$DATASET" ]; then
    DATASET="file://$(realpath "$DATASET")"
fi

echo "========================================================================"
echo "  SUBMITTING QUESTION 14: SMS SPAM DETECTION (NAIVE BAYES) TO SPARK     "
echo "========================================================================"
spark-submit --master "local[*]" sms_spam_naive_bayes.py "$DATASET"
