#!/bin/bash
# ---------------------------------------------------------------------------
# init.sh — Bootstrap a Spring Boot CRUD app from a draw.io diagram
#
# Usage:
#   bash init.sh --diagram <path> --package <java.package> [--app-name <name>] [--port <port>]
#
# Example:
#   bash init.sh \
#     --diagram ../../data/class-diagram-example.drawio \
#     --package org.enspy.snappy.server \
#     --app-name snappy-server \
#     --port 8080
# ---------------------------------------------------------------------------
set -e

# ── Defaults ────────────────────────────────────────────────────────────────
DIAGRAM=""
PACKAGE=""
APP_NAME="generated-app"
PORT=8080
BOOT_VERSION="3.5.0"
JAVA_VERSION="21"

# ── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --diagram)  DIAGRAM="$2";  shift 2 ;;
    --package)  PACKAGE="$2";  shift 2 ;;
    --app-name) APP_NAME="$2"; shift 2 ;;
    --port)     PORT="$2";     shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$DIAGRAM" || -z "$PACKAGE" ]]; then
  echo "Error: --diagram and --package are required."
  echo "Usage: bash init.sh --diagram <path> --package <java.package>"
  exit 1
fi

ARTIFACT=$(echo "$APP_NAME" | tr '.' '-')
GROUP=$(echo "$PACKAGE" | rev | cut -d'.' -f2- | rev)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/$APP_NAME"

echo "============================================================"
echo "  uml2code — Spring Boot init"
echo "  Diagram  : $DIAGRAM"
echo "  Package  : $PACKAGE"
echo "  App name : $APP_NAME"
echo "  Port     : $PORT"
echo "============================================================"
echo ""

# ── Step 1: Download Spring Boot project from Spring Initializr ─────────────
echo "[1/4] Downloading Spring Boot $BOOT_VERSION project..."

curl -sL \
  "https://start.spring.io/starter.zip?\
type=maven-project\
&language=java\
&bootVersion=${BOOT_VERSION}\
&groupId=${GROUP}\
&artifactId=${ARTIFACT}\
&packageName=${PACKAGE}\
&javaVersion=${JAVA_VERSION}\
&dependencies=web,data-jpa,h2,lombok,validation" \
  -o /tmp/spring-init.zip

unzip -q /tmp/spring-init.zip -d "$OUTPUT_DIR"
rm /tmp/spring-init.zip
echo "    -> $OUTPUT_DIR"

# ── Step 2: Add springdoc-openapi dependency to pom.xml ─────────────────────
echo "[2/4] Patching pom.xml (springdoc-openapi)..."

python3 - "$OUTPUT_DIR/pom.xml" <<'PYEOF'
import sys

path = sys.argv[1]
dep = """\t\t<dependency>
\t\t\t<groupId>org.springdoc</groupId>
\t\t\t<artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
\t\t\t<version>2.6.0</version>
\t\t</dependency>"""

content = open(path).read()
patched = content.replace("</dependencies>", dep + "\n\t</dependencies>", 1)
open(path, "w").write(patched)
PYEOF

# ── Step 3: Patch application.properties ────────────────────────────────────
echo "[3/4] Writing application.properties..."

cat > "$OUTPUT_DIR/src/main/resources/application.properties" <<EOF
# Server
server.port=${PORT}
server.forward-headers-strategy=framework

# H2
spring.datasource.url=jdbc:h2:mem:${ARTIFACT}db
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# JPA
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=false

# Springdoc / Swagger
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.api-docs.path=/api-docs
EOF

# ── Step 4: Generate Java source files ──────────────────────────────────────
echo "[4/4] Generating Java source files from diagram..."

python3 "$PROJECT_ROOT/main.py" \
  "$DIAGRAM" \
  --package "$PACKAGE" \
  --output "$OUTPUT_DIR/src/main/java"

echo ""
echo "============================================================"
echo "  Done! To start the application:"
echo ""
echo "  cd $OUTPUT_DIR"
echo "  ./mvnw spring-boot:run"
echo ""
echo "  Swagger UI : http://localhost:${PORT}/swagger-ui/index.html"
echo "  H2 console : http://localhost:${PORT}/h2-console"
echo "============================================================"
