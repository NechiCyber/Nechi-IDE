from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    PYTHON_KEYWORDS = [
        "def", "class", "if", "else", "elif", "while", "for", "return", 
        "import", "from", "try", "except", "finally", "with", "pass", 
        "break", "continue", "True", "False", "None", "self", "and", 
        "or", "not", "is", "in", "lambda", "assert", "global", "nonlocal", "yield", 
        "print", "input"
    ]

    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QColor("#C586C0")) 

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FB4AAE")) 

        library_format = QTextCharFormat()
        library_format.setForeground(QColor("#50FA7B")) 

        library_classes_pattern = r"\b(?!(?:True|False|None)\b)[A-Z][a-zA-Z0-9_]*\b"
        self.rules.append((QRegularExpression(library_classes_pattern), library_format))

        library_methods_pattern = r"\.[a-zA-Z_][a-zA-Z0-9_]*\b"
        self.rules.append((QRegularExpression(library_methods_pattern), library_format))

        import_pattern = r"(?<=import\s)[a-zA-Z_][a-zA-Z0-9_]*|(?<=from\s)[a-zA-Z_][a-zA-Z0-9_]*"
        self.rules.append((QRegularExpression(import_pattern), library_format))

        keywords_pattern = rf"\b(?:{'|'.join(self.PYTHON_KEYWORDS)})\b"
        self.rules.append((QRegularExpression(keywords_pattern), keyword_format))

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.default_format)

        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
      
                start = match.capturedStart()
                length = match.capturedLength()
                if match.captured().startswith('.'):
                    start += 1
                    length -= 1

                self.setFormat(start, length, fmt)
