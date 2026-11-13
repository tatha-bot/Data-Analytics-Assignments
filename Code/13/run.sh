#!/usr/bin/env bash
# ==============================================================================
# Runner Script for Question 13: Bayes' Theorem for Two-Class Classification (Iris)
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATASET="${1:-iris.csv}"

echo "========================================================================"
echo "  SUBMITTING QUESTION 13: BAYES' THEOREM (IRIS 2-CLASS) TO SPARK        "
echo "========================================================================"
spark-submit --master "local[*]" bayes_two_class.py "$DATASET"
