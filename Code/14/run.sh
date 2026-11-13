#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 14: SMS Spam Detection via Spark Naive Bayes
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-spam.csv}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 14: SMS SPAM DETECTION (NAIVE BAYES) TO SPARK     "
echo "========================================================================"
spark-submit --master "local[*]" sms_spam_naive_bayes.py "$DATASET"
