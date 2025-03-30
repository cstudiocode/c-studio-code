import sys
import os 
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenuBar, QMenu, QAction, 
                            QFileDialog, QMessageBox, QTextEdit, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from compiler.compiler import Compiler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compiler = Compiler()
        self.current_file = None
        self._setup_ui()
        self._setup_menubar()
        self._setup_window()
        
    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.setWindowTitle("C Studio Code")
        self.resize(1200, 800)
        
        # Configuration de l'icône
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "icones", "app_icon.ico")
        
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icône introuvable : {icon_path}")
        
        self.setWindowIcon(QIcon(icon_path))

    def _setup_menubar(self):
        """Crée la barre de menus comme VSCode"""
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)
        
        # Menu Edit
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        # Menu Run
        run_menu = menubar.addMenu("&Run")
        
        run_action = QAction("Run", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self._compile_code)
        run_menu.addAction(run_action)
        
        # Menu Help
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About C Studio Code", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_ui(self):
        """Initialise l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Éditeur de code
        self.editor = QTextEdit()
        self.editor.setStyleSheet("""
            QTextEdit {
                font-family: Consolas;
                font-size: 14px;
                background-color: #1E1E1E;
                color: #D4D4D4;
            }
        """)
        layout.addWidget(self.editor)
        
        # Console de sortie
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                font-family: Consolas;
                font-size: 12px;
                background-color: #1E1E1E;
                color: #D4D4D4;
            }
        """)
        layout.addWidget(self.output)

    def _new_file(self):
        """Crée un nouveau fichier"""
        self.editor.clear()
        self.current_file = None
        
    def _open_file(self):
        """Ouvre un fichier existant"""
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            "C Files (*.c *.h);;All Files (*)"
        )
        if path:
            with open(path, 'r') as f:
                self.editor.setText(f.read())
            self.current_file = path
            
    def _save_file(self):
        """Enregistre le fichier courant"""
        if not self.current_file:
            self._save_file_as()
        else:
            with open(self.current_file, 'w') as f:
                f.write(self.editor.text())
                
    def _save_file_as(self):
        """Enregistre sous un nouveau nom"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "C Files (*.c *.h);;All Files (*)"
        )
        if path:
            with open(path, 'w') as f:
                f.write(self.editor.text())
            self.current_file = path
            
    def _compile_code(self):
        """Compile et exécute le code"""
        code = self.editor.text()
        success, errors = self.compiler.compile(code)
        
        if success:
            self._show_output("Compilation réussie !")
        else:
            self._show_output(f"Erreur :\n{errors}")
            
    def _show_output(self, text):
        """Affiche du texte dans la console de sortie"""
        self.output.append(text)
        
    def _show_about(self):
        """Affiche la boîte de dialogue About"""
        QMessageBox.about(
            self,
            "About C Studio Code",
            "C Studio Code v1.0\n\n"
            "A lightweight C IDE\n"
            "© 2025 - Fordi Malanda "
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configuration spécifique Windows pour l'icône
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('cstudiocode.1.0')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())