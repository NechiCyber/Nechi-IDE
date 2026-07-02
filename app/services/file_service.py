import os
import shutil


class FileService:

      def read_file(self, path):
            with open(path, "r", encoding="utf-8") as f:
                  return f.read()

      def write_file(self, path, content):
            with open(path, "w", encoding="utf-8") as f:
                  f.write(content)

      def create_file(self, folder, name):
            path = os.path.join(folder, name)
            open(path, "w").close()
            return path

      def create_folder(self, folder, name):
            path = os.path.join(folder, name)
            os.mkdir(path)
            return path

      def rename(self, path, new_name):
            new_path = os.path.join(os.path.dirname(path), new_name)
            os.rename(path, new_path)
            return new_path

      def delete(self, path):
            if os.path.isdir(path):
                  shutil.rmtree(path)
            else:
                  os.remove(path)