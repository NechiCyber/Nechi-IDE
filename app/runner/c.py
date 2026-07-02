import os
import shutil
import subprocess

def find_c_compiler():
    compilers = ["gcc", "clang", "cl"]
    
    for compiler in compilers:
        path = shutil.which(compiler)
        if path:
            return path
    return None


def run_c(project_path, file_path):
    compiler = find_c_compiler()

    if compiler is None:
        print("C compiler (gcc/clang) not found. Please install a compiler.")
        return

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    if os.name == "nt":
        output_executable = os.path.join(project_path, f"{base_name}.exe")
    else:
        output_executable = os.path.join(project_path, base_name)

    compile_command = [compiler, file_path, "-o", output_executable]
    
    if "cl.exe" in compiler.lower():
        compile_command = [compiler, file_path, f"/Fe:{output_executable}"]

    try:
        result = subprocess.run(
            compile_command,
            cwd=project_path,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            print("Compilation Error:\n", result.stderr)
            return

        subprocess.Popen(
            [output_executable],
            cwd=project_path
        )

    except Exception as e:
        print(f"Failed to run C program: {e}")
