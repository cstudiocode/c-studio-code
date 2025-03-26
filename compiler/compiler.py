import sys
import platform
import subprocess

def get_gcc_path():
    if platform.system() == "Windows":
        return ".compiler/MinGWbin/gcc.exe"
    else:
        return "gcc"


def compile_c(code, output_path):
    gcc = get_gcc_path()
    result = subprocess.run(
        [gcc, "-x", "c", "-", "-o", output_path],
        input=code.encode(),
        capture_output=True
    )
    return result.returncode == 0, result.stderr.decode()