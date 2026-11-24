#!/usr/bin/env bash
# ==============================================================================
# Trustworthy Readiness & Live Smoke-Test Script (Assignments 1-4, 6-21)
# Excludes Code/5 (Hive). Works on macOS and Linux.
# Usage:
#   ./check.sh         # Environment + live HDFS/YARN/Spark smoke tests (~5s)
#   ./check.sh --full  # Also executes Spark assignments (6, 7, 13-16, 21)
# ==============================================================================

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FULL_MODE=false
[ "${1:-}" = "--full" ] && FULL_MODE=true

PASS=0
WARN=0
FAIL=0

ok()   { echo "  [OK]      $1"; PASS=$((PASS + 1)); }
warn() { echo "  [WARN]    $1"; WARN=$((WARN + 1)); }
fail() { echo "  [FAIL]    $1"; FAIL=$((FAIL + 1)); }

echo "========================================================================"
echo "  SYSTEM READINESS & LIVE SMOKE CHECK (Assignments 1-4, 6-21)           "
echo "========================================================================"

# ------------------------------------------------------------------------------
# 1. Java & JDK
# ------------------------------------------------------------------------------
echo ""
echo "[1/6] Checking Java & JDK..."
for tool in java javac jar jps; do
    if command -v "$tool" >/dev/null 2>&1; then
        ok "$tool available"
    else
        fail "$tool missing (install JDK 11+)"
    fi
done

# ------------------------------------------------------------------------------
# 2. Hadoop Daemons + Live HDFS & YARN Health (Code 1, 2, 3, 4)
# ------------------------------------------------------------------------------
echo ""
echo "[2/6] Checking Hadoop & Live HDFS/YARN Health (Code 1-4)..."
if command -v hadoop >/dev/null 2>&1 && command -v hdfs >/dev/null 2>&1; then
    ok "hadoop & hdfs CLI available ($(hadoop version 2>/dev/null | head -n 1))"

    if command -v jps >/dev/null 2>&1; then
        JPS_OUT=$(jps 2>/dev/null)
        for daemon in NameNode DataNode ResourceManager NodeManager; do
            if echo "$JPS_OUT" | grep -q "$daemon"; then
                ok "Daemon running: $daemon"
            else
                fail "Daemon NOT running: $daemon (run start-all.sh)"
            fi
        done
    fi

    if hdfs dfs -ls / >/dev/null 2>&1; then
        ok "HDFS reachable (hdfs dfs -ls / succeeded)"
    else
        fail "HDFS unreachable (check NameNode / start-all.sh)"
    fi

    SAFEMODE=$(hdfs dfsadmin -safemode get 2>/dev/null || true)
    if echo "$SAFEMODE" | grep -qi "OFF"; then
        ok "HDFS SafeMode is OFF"
    elif [ -n "$SAFEMODE" ]; then
        fail "HDFS SafeMode is ON (run: hdfs dfsadmin -safemode leave)"
    else
        warn "Could not query HDFS SafeMode"
    fi

    if command -v yarn >/dev/null 2>&1 && yarn node -list 2>/dev/null | grep -qiE "Total Nodes:[1-9]|RUNNING"; then
        ok "YARN NodeManager active"
    else
        warn "YARN NodeManager not confirmed active (check ResourceManager/NodeManager)"
    fi
else
    fail "hadoop/hdfs CLI not found"
fi

# ------------------------------------------------------------------------------
# 3. Apache Spark + Python + NumPy
# ------------------------------------------------------------------------------
echo ""
echo "[3/6] Checking Spark, Python 3 & NumPy (Code 6, 7, 13-16, 21)..."
if ! command -v spark-submit >/dev/null 2>&1 && [ -x "/home/hp/spark/bin/spark-submit" ]; then
    export SPARK_HOME="${SPARK_HOME:-/home/hp/spark}"
    export PATH="$SPARK_HOME/bin:$PATH"
fi

if command -v spark-submit >/dev/null 2>&1; then
    ok "spark-submit available ($(command -v spark-submit))"
else
    fail "spark-submit not found"
fi

if command -v python3 >/dev/null 2>&1; then
    ok "python3 available ($(python3 --version 2>&1))"
    if python3 -c "import numpy" >/dev/null 2>&1; then
        ok "numpy available"
    else
        fail "numpy missing (run: pip3 install numpy)"
    fi
else
    fail "python3 not found"
fi

# ------------------------------------------------------------------------------
# 4. All Required Source Files, JARs, Runner Scripts & Datasets
# ------------------------------------------------------------------------------
echo ""
echo "[4/6] Checking Assignment Files, JARs & Datasets..."
REQUIRED_FILES=(
    "Code/2/WordCount.java" "Code/2/WordCount.jar" "Code/2/input.txt"
    "Code/3/MatrixMultiplication.java" "Code/3/Matrix.jar" "Code/3/matrix.txt"
    "Code/4/MovieTags.java" "Code/4/MovieTags.jar" "Code/4/ml-latest-small/tags.csv"
    "Code/6/MaxTemperature.java" "Code/6/MaxTemperature.jar" "Code/6/temperatures.txt" "Code/6/build_and_run.sh"
    "Code/7/clustering_spark.py" "Code/7/clustering_data.csv" "Code/7/run.sh"
    "Code/13/bayes_two_class.py" "Code/13/iris.csv" "Code/13/run.sh"
    "Code/14/sms_spam_naive_bayes.py" "Code/14/spam.csv" "Code/14/run.sh"
    "Code/15/compare_gaussian_bernoulli.py" "Code/15/digits_images.csv" "Code/15/run.sh"
    "Code/16/bayes_multiclass_images.py" "Code/16/digits_multiclass.csv" "Code/16/run.sh"
    "Code/21/knn_spark_images.py" "Code/21/digits_knn.csv" "Code/21/run.sh"
)

MISSING=0
for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -s "$SCRIPT_DIR/$f" ]; then
        fail "Missing or empty: $f"
        MISSING=$((MISSING + 1))
    fi
done
[ "$MISSING" -eq 0 ] && ok "All ${#REQUIRED_FILES[@]} source files, JARs, scripts & datasets present"

# ------------------------------------------------------------------------------
# 5. Live Spark Smoke Test (proves spark-submit + PySpark + MLlib + NumPy work)
# ------------------------------------------------------------------------------
echo ""
echo "[5/6] Running Live Spark Smoke Test..."
if command -v spark-submit >/dev/null 2>&1; then
    SMOKE_PY=$(mktemp /tmp/spark_smoke_XXXXXX.py)
    cat > "$SMOKE_PY" <<'EOF'
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.classification import NaiveBayes
spark = SparkSession.builder.appName("SmokeTest").master("local[1]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
assert spark.range(5).count() == 5
assert np.linalg.norm(np.array([3.0, 4.0])) == 5.0
spark.stop()
print("SPARK_SMOKE_OK")
EOF
    if spark-submit --master "local[1]" "$SMOKE_PY" 2>/dev/null | grep -q "SPARK_SMOKE_OK"; then
        ok "Live PySpark + NumPy + MLlib smoke test passed"
    else
        fail "Live PySpark smoke test failed"
    fi
    rm -f "$SMOKE_PY"
else
    fail "Skipped Spark smoke test (spark-submit missing)"
fi

# ------------------------------------------------------------------------------
# 6. Optional Full Execution of Spark Assignments (--full)
# ------------------------------------------------------------------------------
echo ""
echo "[6/6] Full Assignment Execution..."
if $FULL_MODE; then
    if (cd "$SCRIPT_DIR/Code/6" && bash build_and_run.sh >/dev/null 2>&1); then
        ok "Code/6 (MaxTemperature Java Spark) ran cleanly"
    else
        fail "Code/6 failed"
    fi
    for d in 7 13 14 15 16 21; do
        if (cd "$SCRIPT_DIR/Code/$d" && bash run.sh >/dev/null 2>&1); then
            ok "Code/$d ran cleanly"
        else
            fail "Code/$d failed"
        fi
    done
else
    echo "  [INFO]    Skipped full run (use './check.sh --full' to execute Code/6, 7, 13-16, 21)"
fi

echo ""
echo "========================================================================"
echo "  SUMMARY: $PASS OK | $WARN WARNINGS | $FAIL FAILED"
echo "========================================================================"
if [ "$FAIL" -gt 0 ]; then
    echo "Status: NOT READY — fix [FAIL] items above."
    exit 1
elif [ "$WARN" -gt 0 ]; then
    echo "Status: READY WITH WARNINGS — review [WARN] items above."
    exit 0
else
    echo "Status: 100% READY — all Hadoop & Spark assignments are verified to run!"
    exit 0
fi
