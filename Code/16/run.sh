#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 16: Bayes' Theorem for Multiclass Image Classification
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-digits_multiclass.csv}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 16: MULTICLASS BAYES' THEOREM (DIGITS) TO SPARK   "
echo "========================================================================"
spark-submit --master "local[*]" bayes_multiclass_images.py "$DATASET"
