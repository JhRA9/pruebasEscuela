#!/usr/bin/env python3
import os
import subprocess
import sys

# Configuración (ajusta aquí tus tokens)
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "TU_TOKEN_SONAR")
CODACY_PROJECT_TOKEN = os.getenv("CODACY_PROJECT_TOKEN", "TU_TOKEN_CODACY")

# Parámetros comunes
SONAR_HOST = "http://localhost:9000"
FILE = "controler_login.php"

def run_sonar():
    print(f"\n=== SonarQube Analysis: {FILE} ===\n")
    cmd = [
        "sonar-scanner",
        f"-Dsonar.projectKey=sistemaescolar-login",
        f"-Dsonar.host.url={SONAR_HOST}",
        f"-Dsonar.login={SONAR_TOKEN}",
        f"-Dsonar.sources=./{FILE}",
        f"-Dsonar.inclusions={FILE}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

def run_codacy():
    print(f"\n=== Codacy Analysis: {FILE} ===\n")
    # Instala CLI si hace falta
    if not os.path.isfile("./codacy-analysis-cli"):
        subprocess.run(
            ["curl", "-LsSf", "https://api.codacy.com/cli/install.sh", "|", "sh"],
            shell=True
        )
    os.environ["CODACY_PROJECT_TOKEN"] = CODACY_PROJECT_TOKEN
    cmd = [
        "./codacy-analysis-cli", "analyze",
        "--project-token", CODACY_PROJECT_TOKEN,
        "--patterns", FILE
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    run_sonar()
    run_codacy()
