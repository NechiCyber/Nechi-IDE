from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

class CHighlighter(QSyntaxHighlighter):
    C_KEYWORDS = [
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "goto", "if",
        "int", "long", "register", "return", "short", "signed", "sizeof", "static",
        "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
        "_Alignas", "_Alignof", "_Atomic", "_Bool", "_Complex", "_Generic", "_Imaginary",
        "_Noreturn", "_Static_assert", "_Thread_local", "inline", "restrict"
    ]

    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QColor("#C586C0")) 

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF79C6")) 

        library_format = QTextCharFormat()
        library_format.setForeground(QColor("#50FA7B")) 

        function_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()"
        self.rules.append((QRegularExpression(function_pattern), library_format))

        include_file_pattern = r'(?<=#include\s)(?:<[^>]+>|"[^"]+")'
        self.rules.append((QRegularExpression(include_file_pattern), library_format))

        library_types_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*_t\b|\bFILE\b"
        self.rules.append((QRegularExpression(library_types_pattern), library_format))

        preprocessor_pattern = r"#[a-zA-Z_][a-zA-Z0-9_]*"
        self.rules.append((QRegularExpression(preprocessor_pattern), library_format))

        keywords_pattern = rf"\b(?:{'|'.join(self.C_KEYWORDS)})\b"
        self.rules.append((QRegularExpression(keywords_pattern), keyword_format))

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.default_format)

        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    fmt
                )
