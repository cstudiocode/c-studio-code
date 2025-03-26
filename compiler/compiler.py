# compiler.py
import os
from PyQt5.QtWidgets import QFileDialog

class Compiler:
    def __init__(self):
        self.gcc_path = self.detect_gcc()

    def detect_gcc(self):
        # Cherche GCC dans l'ordre : chemin custom → système
        custom_path = "./compiler/MinGW/gcc/bin/gcc.exe"
        if os.path.exists(custom_path):
            return custom_path
        return "gcc"  # Fallback système

    def compile(self, code, output_dir):
        output_path = os.path.join(output_dir, "program")
        cmd = [self.gcc_path, "-o", output_path, "-x", "c", "-"]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, stderr = process.communicate(input=code.encode())
        return process.returncode == 0, stderr.decode()
    
# Pour inclure GCC si bundlé
datas = [("compiler/gcc", "compiler/gcc")]