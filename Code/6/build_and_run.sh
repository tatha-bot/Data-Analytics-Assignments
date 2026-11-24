#!/usr/bin/env bash
# ==============================================================================
# Build and Run Script for Question 6: Maximum Temperature in Spark using Java
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================================"
echo "  COMPILING AND RUNNING QUESTION 6: MAX TEMPERATURE (SPARK JAVA)        "
echo "========================================================================"

# Determine Spark home and JARs location
if [ -z "$SPARK_HOME" ] || [ ! -d "$SPARK_HOME/jars" ]; then
    if [ -d "/home/hp/spark/jars" ]; then
        export SPARK_HOME="/home/hp/spark"
    elif [ -d "/opt/homebrew/opt/apache-spark/libexec/jars" ]; then
        export SPARK_HOME="/opt/homebrew/opt/apache-spark/libexec"
    elif [ -d "/usr/local/Cellar/apache-spark" ]; then
        SPARK_LIB_FOUND=$(find /usr/local/Cellar/apache-spark -type d -name "jars" | head -n 1)
        export SPARK_HOME="$(dirname "$SPARK_LIB_FOUND")"
    fi
fi

if [ -n "$SPARK_HOME" ] && [ -d "$SPARK_HOME/jars" ]; then
    SPARK_LIB="$SPARK_HOME/jars"
    if ! command -v spark-submit >/dev/null 2>&1 && [ -x "$SPARK_HOME/bin/spark-submit" ]; then
        export PATH="$SPARK_HOME/bin:$PATH"
    fi
else
    echo "Error: Could not locate Spark JARs directory. Please ensure SPARK_HOME is set."
    exit 1
fi

echo "[1/3] Using Spark libraries from: $SPARK_LIB"
CLASSPATH=$(echo "$SPARK_LIB"/*.jar | tr ' ' ':')

if command -v javac >/dev/null 2>&1; then
    # Clean old artifacts
    mkdir -p build
    rm -f build/*.class MaxTemperature.jar

    # Compile Java source
    echo "[2/3] Compiling MaxTemperature.java..."
    javac -cp "$CLASSPATH" -d build MaxTemperature.java

    # Create JAR
    jar cf MaxTemperature.jar -C build .
    echo "Created MaxTemperature.jar successfully."
elif [ -f "MaxTemperature.jar" ]; then
    echo "[2/3] javac not found; using pre-built MaxTemperature.jar..."
else
    echo "Error: javac not found and pre-built MaxTemperature.jar is missing."
    exit 1
fi

# Execute via spark-submit
INPUT_FILE="temperatures.txt"
if [ "$#" -ge 1 ]; then
    INPUT_FILE="$1"
fi

if [[ "$INPUT_FILE" != *"://"* ]] && [ -e "$INPUT_FILE" ]; then
    INPUT_FILE="file://$(realpath "$INPUT_FILE")"
fi

echo "[3/3] Submitting application to Apache Spark..."
spark-submit --class MaxTemperature MaxTemperature.jar "$INPUT_FILE"
