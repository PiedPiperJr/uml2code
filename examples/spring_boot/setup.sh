#!/bin/bash
# ---------------------------------------------------------------------------
# setup.sh — Install prerequisites for the Spring Boot example
#
# Run this once before using init.sh:
#   bash setup.sh
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Installing Java 21 ==="
sudo apt-get update -q
sudo apt-get install -y openjdk-21-jdk

echo "=== Installing Maven ==="
sudo apt-get install -y maven

echo "=== Configuring JAVA_HOME ==="
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

echo "=== Installing Python dependencies ==="
pip install -r "$PROJECT_ROOT/requirements.txt"

echo ""
echo "=== Versions ==="
java -version
mvn -version
python3 --version

echo ""
echo "Setup complete. You can now run init.sh."
