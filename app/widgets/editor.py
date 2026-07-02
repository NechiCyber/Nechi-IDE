# app/widgets/editor.py

from app.widgets.code_editor import CodeEditor

from PySide6.QtGui import QFont

from PySide6.QtGui import QFont

def create_editor():
    editor = CodeEditor()

    # 1. Сначала настраиваем шрифт
    font = QFont("JetBrains Mono", 13)
    font.setStyleHint(QFont.StyleHint.Monospace)
    editor.setFont(font)

    # 2. Теперь рассчитываем табы (6 пробелов выбранного шрифта JetBrains Mono)
    editor.setTabStopDistance(
        editor.fontMetrics().horizontalAdvance(" ") * 6
    )

    # 3. Применяем стили (изменили селектор на QPlainTextEdit, чтобы стили точно сработали)
    editor.setStyleSheet("""
        QPlainTextEdit {
            background-color: #1E1E1E;
            color: #D4D4D4;
            border: none;
            selection-background-color: #264F78;
        }
    """)

    return editor
