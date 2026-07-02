import sys
import os

from PySide6.QtWidgets import (
      QWidget, QPushButton, QVBoxLayout,
      QFileDialog, QApplication
)
from PySide6.QtGui import (
      QFont
)

from app.window import MainWindow


class WelcomeWindow(QWidget):

      def __init__(self):
            super().__init__()

            self.setWindowTitle("NIDE")
            self.resize(600, 350)

            layout = QVBoxLayout()

            self.open_btn = QPushButton("Open Folder")
            self.exit_btn = QPushButton("Exit")
            
            self.open_btn.setFont(QFont("JetBrains Mono", 18))
            self.exit_btn.setFont(QFont("JetBrains Mono", 18))
            
            self.open_btn.setMinimumHeight(100)
            self.exit_btn.setMinimumHeight(100)

            self.open_btn.clicked.connect(self.open_folder)
            self.exit_btn.clicked.connect(self.close_app)

            layout.addWidget(self.open_btn)
            layout.addWidget(self.exit_btn)

            self.setLayout(layout)

      def open_folder(self):

            folder = QFileDialog.getExistingDirectory(
                  self,
                  "Open Project Folder"
            )

            if not folder:
                  return

            self.main = MainWindow(folder)
            self.main.show()
            self.close()

      def close_app(self):
            QApplication.quit()