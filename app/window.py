from PySide6.QtWidgets import (
    QMainWindow, QMessageBox,
    QSplitter, QMenu,
    QInputDialog, QFileDialog
)

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence

from app.explorer.controller import ExplorerController
from app.widgets.file_model import FileSystemModel

from app.widgets.editor import create_editor
from app.menus.file_menu import create_file_menu

from app.actions.file import save, save_as
from app.actions.restart import restart

from app.runner.manager import run
from app.syntax.python import PythonHighlighter

from app.terminal.terminal import Terminal


class MainWindow(QMainWindow):

    def __init__(self, project_path):
        super().__init__()

        # PROJECT PATH
        self.project_path = project_path

        self.setWindowTitle("NIDE")
        self.resize(1000, 800)

        # ---------------- EDITOR ----------------
        self.editor = create_editor()
        self.current_file = None

        self.editor.document().modificationChanged.connect(
            lambda _: self.update_title()
        )

        # ---------------- MODEL + EXPLORER ----------------
        self.model = FileSystemModel()
        self.model.setRootPath(self.project_path)

        self.explorer = ExplorerController(self, self.model)
        self.tree = self.explorer.tree
        
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        self.tree.setRootIndex(
            self.model.index(self.project_path)
        )

        # ---------------- TERMINAL ----------------
        self.terminal = Terminal()

        # ---------------- TOOLBAR ----------------
        toolbar = self.addToolBar("Run")

        run_action = toolbar.addAction("▶ Run")
        restart_action = toolbar.addAction("⟳ Restart")

        run_action.triggered.connect(lambda: run(self))
        restart_action.triggered.connect(restart)

        # ---------------- SHORTCUTS ----------------
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(
            lambda: save(self, self.editor)
        )

        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(
            lambda: save_as(self, self.editor)
        )

        # ---------------- SPLITTERS ----------------
        horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)

        horizontal_splitter.addWidget(self.tree)
        horizontal_splitter.addWidget(self.editor)
        horizontal_splitter.setStretchFactor(1, 1)
        horizontal_splitter.setSizes([250, 750])

        vertical_splitter = QSplitter(Qt.Orientation.Vertical)

        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(self.terminal)
        vertical_splitter.setStretchFactor(0, 1)
        vertical_splitter.setSizes([600, 200])

        self.setCentralWidget(vertical_splitter)

        # ---------------- MENU ----------------
        menu_bar = self.menuBar()
        create_file_menu(self, menu_bar, self.editor)

    # ---------------- CLOSE EVENT ----------------
    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    # ---------------- TITLE ----------------
    def update_title(self):
        if self.current_file is None:
            self.setWindowTitle("NIDE")
            return

        name = os.path.basename(self.current_file)

        if self.editor.document().isModified():
            name += "*"

        self.setWindowTitle(f"NIDE - {name}")

    # ---------------- SAVE CHECK ----------------
    def maybe_save(self):

        if not self.editor.document().isModified():
            return True

        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            f"Save changes to {os.path.basename(self.current_file) if self.current_file else 'Untitled'}?",
            QMessageBox.Yes |
            QMessageBox.No |
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:

            save(self, self.editor)
            return not self.editor.document().isModified()

        if reply == QMessageBox.No:
            return True

        return False