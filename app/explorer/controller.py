import os

from PySide6.QtWidgets import QTreeView, QMenu, QInputDialog, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.syntax.python import PythonHighlighter
from app.syntax.c import CHighlighter
from app.services.file_service import FileService


class ExplorerController:

      def __init__(self, window, model):
            self.window = window
            self.model = model
            self.fs = FileService()

            self.tree = QTreeView()
            self.tree.setModel(model)
            
            self.tree.setFont(QFont("JetBrains Mono", 13))

            self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.tree.customContextMenuRequested.connect(self.open_context_menu)
            self.tree.clicked.connect(self.open_file)

      # ---------------- OPEN FILE ----------------
      def open_file(self, index):

            if not self.window.maybe_save():
                  return

            if self.model.isDir(index):
                  return

            file_path = self.model.filePath(index)

            content = self.fs.read_file(file_path)

            self.window.editor.setPlainText(content)

            self.window.current_file = file_path
            self.window.editor.document().setModified(False)

            if file_path.endswith(".py"):
                  self.window.highlighter = PythonHighlighter(
                        self.window.editor.document()
                  )
            
            elif file_path.endswith(".c"):
                  self.window.highlighter = CHighlighter(
                        self.window.editor.document()
                  )
            
            else:
                  self.window.highlighter = None

      # ---------------- CONTEXT MENU ----------------
      def open_context_menu(self, position):

            index = self.tree.indexAt(position)

            file_path = None
            if index.isValid():
                  file_path = self.model.filePath(index)

            menu = QMenu()

            new_file = menu.addAction("New File")
            new_folder = menu.addAction("New Folder")
            menu.addSeparator()
            rename = menu.addAction("Rename")
            delete = menu.addAction("Delete")

            action = menu.exec(self.tree.viewport().mapToGlobal(position))

            if action == new_file:
                  self.create_new_file(file_path)

            elif action == new_folder:
                  self.create_new_folder(file_path)

            elif action == rename and index.isValid():
                  self.rename_item(file_path)

            elif action == delete and index.isValid():
                  self.delete_item(file_path)

      # ---------------- CREATE FILE ----------------
      def create_new_file(self, path):

            folder = self.window.project_path
            if path:
                  folder = path if os.path.isdir(path) else os.path.dirname(path)

            name, ok = QInputDialog.getText(self.window, "New File", "File name:")
            if not ok or not name:
                  return

            self.fs.create_file(folder, name)

      # ---------------- CREATE FOLDER ----------------
      def create_new_folder(self, path):

            folder = self.window.project_path
            if path:
                  folder = path if os.path.isdir(path) else os.path.dirname(path)

            name, ok = QInputDialog.getText(self.window, "New Folder", "Folder name:")
            if not ok or not name:
                  return

            self.fs.create_folder(folder, name)

      # ---------------- RENAME ----------------
      def rename_item(self, path):

            new_name, ok = QInputDialog.getText(self.window, "Rename", "New name:")
            if not ok or not new_name:
                  return

            self.fs.rename(path, new_name)

      # ---------------- DELETE ----------------
      def delete_item(self, path):

            reply = QMessageBox.question(
                  self.window,
                  "Delete",
                  f"Delete {os.path.basename(path)}?",
                  QMessageBox.Yes | QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                  return

            self.fs.delete(path)