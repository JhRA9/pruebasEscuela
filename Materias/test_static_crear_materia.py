#!/usr/bin/env python3
import os, subprocess, sys

SONAR_TOKEN = os.getenv("SONAR_TOKEN", "TU_TOKEN_SONAR")
CODACY_PROJECT_TOKEN = os.getenv("CODACY_PROJECT_TOKEN", "TU_TOKEN_CODACY")
SONAR_HOST = "http://localhost:9000"
FILE = "admin/materias/create.php"

def run_sonar():
    print(f"\n=== SonarQube Analysis: {FILE} ===\n")
    subprocess.run([
        "sonar-scanner",
        "-Dsonar.projectKey=sistemaescolar-crear-materia",
        f"-Dsonar.host.url={SONAR_HOST}",
        f"-Dsonar.login={SONAR_TOKEN}",
        f"-Dsonar.sources=./{FILE}",
        f"-Dsonar.inclusions={FILE}"
    ])

def run_codacy():
    print(f"\n=== Codacy Analysis: {FILE} ===\n")
    if not os.path.isfile("./codacy-analysis-cli"):
        subprocess.run(
            ["curl", "-LsSf", "https://api.codacy.com/cli/install.sh", "|", "sh"],
            shell=True
        )
    os.environ["CODACY_PROJECT_TOKEN"] = CODACY_PROJECT_TOKEN
    subprocess.run([
        "./codacy-analysis-cli", "analyze",
        "--project-token", CODACY_PROJECT_TOKEN,
        "--patterns", FILE
    ])

if __name__ == "__main__":
    run_sonar()
    run_codacy()
