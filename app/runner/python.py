import os
import shutil
import subprocess

def find_python(project_path):
    candidates = [
        os.path.join(project_path, ".venv", "bin", "python"),
        os.path.join(project_path, "venv", "bin", "python"),
    ]

    # Windows
    candidates += [
        os.path.join(project_path, ".venv", "Scripts", "python.exe"),
        os.path.join(project_path, "venv", "Scripts", "python.exe"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return shutil.which("python3") or shutil.which("python")


def run_python(project_path, file_path):
    python = find_python(project_path)

    if python is None:
        print("Python interpreter not found.")
        return

    subprocess.Popen(
        [python, file_path],
        cwd=project_path
    )