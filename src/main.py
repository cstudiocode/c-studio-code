import sys
import os 
from PyQt5.QtWidgets import QMainWindow, QApplication  # Import des widgets
from PyQt5.QtGui import QIcon  # Import pour les icônes
from compiler.compiler import Compiler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compiler = Compiler()
        self._setup_ui()
        self.setWindowTitle("C Studio Code")  # Titre de la fenêtre
        self.resize(800, 600)  # Taille par défaut
        # Chemin ABSOLU vers l'icône
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "icones", "app_icon.ico")
        # Vérification critique
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icône introuvable : {icon_path}")
        
        self.setWindowIcon(QIcon(icon_path))

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