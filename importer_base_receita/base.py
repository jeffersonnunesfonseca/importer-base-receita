import os
from zipfile import ZipFile

class FileProcessor():
    
    def __init__(self) -> None:
        self._workspace = "./tmp/"
    
    def create_folder(self, path):
        os.mkdir(path)
    
    def remove_folder(self, path):
        os.remove(path)
            
    def unzip(self, filepath, destiny):
        extracted_files = []
        with ZipFile(filepath, "r") as fzip:
            for filename in fzip.namelist():
                fzip.extract(filename, destiny)
                extracted_files.append(f"{destiny}/{filename}")
        return extracted_files 
