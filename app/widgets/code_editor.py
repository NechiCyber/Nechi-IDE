from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtCore import Qt

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Переменная для включения Python-отступов
        self.use_python_indent = True  # Изменил на True, чтобы авто-табы работали по умолчанию

        # Словарь соответствия для автоматического закрытия скобок и кавычек
        self.brackets_map = {
            '(': ')',
            '{': '}',
            '[': ']',
            '"': '"',
            "'": "'"
        }

    def keyPressEvent(self, event: QKeyEvent):
        text = event.text()
        cursor = self.textCursor()

        # 1. Замена клавиши Tab на 4 пробела (если включен use_python_indent)
        if self.use_python_indent and event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return

        # 2. Автозакрытие скобок и кавычек
        if text in self.brackets_map:
            closing_bracket = self.brackets_map[text]
            
            # Вставляем пару символов
            cursor.insertText(text + closing_bracket)
            
            # Возвращаем курсор назад на 1 позицию (внутрь скобок)
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 1)
            self.setTextCursor(cursor)
            return

        # 3. Умный прыжок через уже существующую закрывающую скобку/кавычку
        if text in self.brackets_map.values():
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
            next_char = cursor.selectedText()
            
            if next_char == text:
                cursor.clearSelection()
                self.setTextCursor(cursor)
                return

        # 4. Вызов стандартного поведения для всех остальных клавиш
        super().keyPressEvent(event)
