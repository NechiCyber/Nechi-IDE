from app.actions.file import (
      new_file,
      open_file,
      save,
      save_as,
      exit_program
)

from app.actions.file import open_folder

def create_file_menu(window, menu_bar, editor):
      file_menu = menu_bar.addMenu("File")
      
      new_action = file_menu.addAction("New")
      open_action = file_menu.addAction("Open")
      open_folder_action = file_menu.addAction("Open Folder")
      save_action = file_menu.addAction("Save")
      save_as_action = file_menu.addAction("Save as")
      exit_action = file_menu.addAction("Exit")
     
      
      new_action.triggered.connect(
            lambda: new_file(window, editor)
      )
      
      open_action.triggered.connect(
            lambda: open_file(window, editor)
      )

      open_folder_action.triggered.connect(
            lambda: open_folder(window)
      )

      exit_action.triggered.connect(
            lambda: exit_program(window)
      )
      
      save_action.triggered.connect(
            lambda: save(window, editor)
      )

      save_as_action.triggered.connect(
            lambda: save_as(window, editor)
      )