from PySide6.QtWidgets import (
      QWidget,
      QVBoxLayout,
      QPlainTextEdit,
      QLineEdit
)

from PySide6.QtGui import QTextCursor

from PySide6.QtCore import QTimer

from app.terminal.shell import Shell

class Terminal(QWidget):
      
      def __init__(self):
            super().__init__()
            
            self.shell = Shell()
            
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            self.output = QPlainTextEdit()
            self.output.setReadOnly(True)
            
            self.input = QLineEdit()
            self.input.setPlaceholderText("Enter command...")
            
            layout.addWidget(self.output)
            layout.addWidget(self.input)
            
            self.input.returnPressed.connect(self.execute)
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.read_shell)
            self.timer.start(20)
      
      def execute(self):
            command = self.input.text()
            
            if not command:
                  return
            
            self.output.appendPlainText(f"$ {command}")
            
            self.shell.write(command + "\n")
            
            self.input.clear()
            
      def read_shell(self):
            
            try:
                  text = self.shell.read()
                  
                  if text:
                        self.output.moveCursor(
                              QTextCursor.MoveOperation.End
                        )
                        self.output.insertPlainText(text)
                        
            except BlockingIOError:
                  pass
            
            except OSError:
                  pass
            
            