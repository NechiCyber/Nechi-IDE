import os

from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtGui import QIcon


class FileSystemModel(QFileSystemModel):
      
      def data(self, index, role):
            
            if role == 1:
                  path = self.filePath(index)
                  
                  if self.isDir(index):
                        return QIcon("assets/icons/folder-aws.svg")
                  
                  ext = os.path.splitext(path)[1]
                  
                  if ext == ".py":
                        return QIcon("assets/icons/python.svg")
                  
                  elif ext == ".c":
                        return QIcon("assets/icons/c.svg")
                  
                  return QIcon("assets/icons/file.svg")
                  
            return super().data(index, role)