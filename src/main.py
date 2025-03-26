from compiler.compiler import Compiler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compiler = Compiler()  # Initialise le compilateur
        self._setup_ui()

    def _compile_code(self):
        code = self.editor.text()
        success, errors = self.compiler.compile(code)
        
        if success:
            self._show_output("Compilation réussie !")
        else:
            self._show_output(f"Erreur :\n{errors}")