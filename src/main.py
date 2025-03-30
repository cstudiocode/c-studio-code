import sys
from PyQt5.QtWidgets import QMainWindow, QApplication  # Import manquant
from compiler.compiler import Compiler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compiler = Compiler()
        self._setup_ui()
        self.setWindowTitle("C Studio Code")  # Titre de la fenêtre
        self.resize(800, 600)  # Taille par défaut

    def _setup_ui(self):
        """Initialise l'interface utilisateur"""
        # ... (votre code d'interface existant)

    def _compile_code(self):
        code = self.editor.text()
        success, errors = self.compiler.compile(code)
        
        if success:
            self._show_output("Compilation réussie !")
        else:
            self._show_output(f"Erreur :\n{errors}")

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crée l'application Qt
    window = MainWindow()         # Crée la fenêtre principale
    window.show()                 # Affiche la fenêtre
    sys.exit(app.exec_())         # Lance la boucle d'événements