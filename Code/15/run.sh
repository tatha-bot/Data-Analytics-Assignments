#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 15: Compare Gaussian and Bernoulli Naive Bayes
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-digits_images.csv}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 15: GAUSSIAN VS BERNOULLI NAIVE BAYES TO SPARK    "
echo "========================================================================"
spark-submit --master "local[*]" compare_gaussian_bernoulli.py "$DATASET"
