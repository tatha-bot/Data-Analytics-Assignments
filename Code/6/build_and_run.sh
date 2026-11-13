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

# Determine Spark JARs location
if [ -n "$SPARK_HOME" ] && [ -d "$SPARK_HOME/jars" ]; then
    SPARK_LIB="$SPARK_HOME/jars"
elif [ -d "/opt/homebrew/opt/apache-spark/libexec/jars" ]; then
    SPARK_LIB="/opt/homebrew/opt/apache-spark/libexec/jars"
elif [ -d "/usr/local/Cellar/apache-spark" ]; then
    SPARK_LIB=$(find /usr/local/Cellar/apache-spark -type d -name "jars" | head -n 1)
else
    echo "Error: Could not locate Spark JARs directory. Please ensure SPARK_HOME is set."
    exit 1
fi

echo "[1/3] Using Spark libraries from: $SPARK_LIB"
CLASSPATH=$(echo "$SPARK_LIB"/*.jar | tr ' ' ':')

# Clean old artifacts
mkdir -p build
rm -f build/*.class MaxTemperature.jar

# Compile Java source
echo "[2/3] Compiling MaxTemperature.java..."
javac -cp "$CLASSPATH" -d build MaxTemperature.java

# Create JAR
jar cf MaxTemperature.jar -C build .
echo "Created MaxTemperature.jar successfully."

# Execute via spark-submit
INPUT_FILE="temperatures.txt"
if [ "$#" -ge 1 ]; then
    INPUT_FILE="$1"
fi

echo "[3/3] Submitting application to Apache Spark..."
spark-submit --class MaxTemperature MaxTemperature.jar "$INPUT_FILE"
