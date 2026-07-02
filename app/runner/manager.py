import os

from app.runner.python import run_python
from app.runner.c import run_c

def run(window):
    if window.current_file is None:
        return

    extension = os.path.splitext(window.current_file)[1]

    if extension == ".py":
        run_python(
            window.project_path,
            window.current_file
        )
    elif extension == ".c":
        run_c(
            window.project_path,
            window.current_file
        )