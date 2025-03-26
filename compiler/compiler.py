import os
import subprocess
import platform
from PyQt5.QtCore import QProcess

class Compiler:
    def __init__(self):
        self.gcc_path = self._detect_gcc()
        self.process = QProcess()
        self.process.readyReadStandardError.connect(self._on_compiler_error)

    def _detect_gcc(self):
        """Détecte le chemin de GCC selon l'OS."""
        # Chemin relatif pour GCC embarqué
        local_paths = {
            'Windows': './compiler/MinGW/bin/gcc.exe',
            'Linux': '/usr/bin/gcc',
            'Darwin': '/usr/local/bin/gcc'
        }
        
        # Priorité au GCC embarqué sous Windows
        if platform.system() == 'Windows' and os.path.exists(local_paths['Windows']):
            return local_paths['Windows']
        
        # Fallback au GCC système
        return local_paths.get(platform.system(), 'gcc')

    def compile(self, code, output_dir="output"):
        """Compile le code C et retourne (succès, erreurs)."""
        output_path = os.path.join(output_dir, 'program')
        os.makedirs(output_dir, exist_ok=True)
        
        # Écrit le code dans un fichier temporaire
        tmp_file = os.path.join(output_dir, 'temp.c')
        with open(tmp_file, 'w') as f:
            f.write(code)
        
        # Commande de compilation
        cmd = [self.gcc_path, tmp_file, '-o', output_path]
        
        # Exécution synchrone
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30s
            )
            return (result.returncode == 0, result.stderr)
        except subprocess.TimeoutExpired:
            return (False, "Erreur: Timeout de compilation")

    def _on_compiler_error(self):
        """Slot pour les erreurs de compilation asynchrones."""
        error = self.process.readAllStandardError().data().decode()
        if error:
            print(f"Erreur de compilation : {error}")