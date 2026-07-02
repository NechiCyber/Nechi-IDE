import sys

from PySide6.QtWidgets import QApplication

from app.welcome import WelcomeWindow

def main():
      app = QApplication(sys.argv)
      
      app.setStyleSheet("""
      QMainWindow {
            background-color: #1E1E1E;
      }

      QWidget {
            background-color: #1E1E1E;
            color: #D4D4D4;
      }

      QMenuBar {
            background-color: #252526;
            color: white;
      }

      QMenuBar::item:selected {
            background-color: #37373D;
      }

      QMenu {
            background-color: #252526;
            color: white;
      }

      QMenu::item:selected {
            background-color: #37373D;
      }

      QTreeView {
            background-color: #252526;
            color: white;
            border: none;
      }

      QTextEdit {
            background-color: #1E1E1E;
            color: #D4D4D4;
            border: none;
            selection-background-color: #264F78;
      }

      QSplitter::handle {
            background-color: #3C3C3C;
      }

      QScrollBar:vertical {
            background: #252526;
            width: 12px;
      }

      QScrollBar::handle:vertical {
            background: #555555;
      }

      QScrollBar::handle:vertical:hover {
            background: #777777;
      }
      """)
      
      window = WelcomeWindow()
      window.show()
      
      app.exec()