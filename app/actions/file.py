from PySide6.QtWidgets import QFileDialog, QMessageBox

def new_file(window, editor):
      if editor.document().isModified():
            reply = QMessageBox.question(
                  window,
                  "Unsaved Changes",
                  "Do you want to save changes before creating a new file?",
                  QMessageBox.Yes |
                  QMessageBox.No |
                  QMessageBox.Cancel
            )

            if reply == QMessageBox.Yes:
                  save(window, editor)

                  if editor.document().isModified():
                        return  # пользователь отменил Save As

                  elif reply == QMessageBox.Cancel:
                        return
      if not window.maybe_save():
            return

      editor.clear()
      window.current_file = None
      window.update_title()
      editor.document().setModified(False)

def open_file(window, editor):
      file_path, _ = QFileDialog.getOpenFileName(
            window,
            "Open File",
            "",
            "All Files (*.*)"
      )
      
      if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                  editor.setPlainText(file.read())

            if not window.maybe_save():
                  return
            
            window.current_file = file_path
            window.update_title()
            editor.document().setModified(False)
                  
def exit_program(window):
      window.close()
      
def save(window, editor):
      if window.current_file is None:
            save_as(window, editor)
            return
      
      with open(window.current_file, "w", encoding="utf-8") as file:
            file.write(editor.toPlainText())
            
      editor.document().setModified(False)
      window.update_title()
      
def save_as(window, editor):
      file_path, _ = QFileDialog.getSaveFileName(
            window,
            "Save File",
            "",
            "All Files (*.*)"
      )
      
      if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                  file.write(editor.toPlainText())
                  
            window.current_file = file_path
            editor.document().setModified(False)
            
def open_folder(window):
      folder = QFileDialog.getExistingDirectory(
            window,
            "Open Folder",
            ""
      )
      
      if not folder:
            return
      
      window.project_path = folder
      
      # update explorer
      window.model.setRootPath(folder)
      window.tree.setRootIndex(window.model.index(folder))