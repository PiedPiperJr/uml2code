#!/bin/bash
set -e

echo "=== Installing Java 21 ==="
sudo apt-get update -q
sudo apt-get install -y openjdk-21-jdk

echo "=== Installing Maven ==="
sudo apt-get install -y maven

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo ""
echo "=== Versions ==="
java -version
mvn -version
python3 --version

echo ""
echo "Setup complete."
