"""Сборка релизного артефакта: архив исходников + отчёт о тестах."""
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

PROJECT_NAME = "KS"
BUILD_DIR = Path("dist")


def run_tests():
    """Прогоняем тесты и сохраняем отчёт в файл."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--junitxml=dist/test-report.xml"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        raise SystemExit("Тесты провалены — релиз прерывается")
    print("Все тесты пройдены")


def make_archive():
    BUILD_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = BUILD_DIR / f"{PROJECT_NAME}-{timestamp}.zip"

    exclude_dirs = {"venv", ".git", ".pytest_cache", "dist", "__pycache__"}
    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in Path(".").rglob("*"):
            if any(part in exclude_dirs for part in path.parts):
                continue
            if path.is_file():
                zf.write(path, path)

    print(f"Артефакт создан: {archive_name}")
    return archive_name


if __name__ == "__main__":
    run_tests()
    make_archive()
