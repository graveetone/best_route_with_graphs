import shutil
import os

class ResetFolderService:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def call(self):
        try:
            shutil.rmtree(self.folder_path)
        except Exception as e:
            ...
        os.mkdir(self.folder_path)
