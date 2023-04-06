import os
from datetime import datetime 

class File:
    def __init__(self, name: str, path: str):
        self.__name = name 
        self.__path = path
        self.__date = self.get_date()
        self.__extension = self.get_extension()

    def __str__(self):
        return f"Filename: {self.__name} \nFilepath: {self.__path}\nCreation date: {self.__date}\nExtension: {self.__extension}\n"

    @property
    def name(self):
        return self.__name 
    
    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    def get_date(self):
        unix_date = int(os.stat(self.__path).st_birthtime)
        date = datetime.utcfromtimestamp(unix_date).strftime("%y%m%d")
        return date
    
    def get_extension(self):
        index = self.__name.rfind(".")
        extension = self.__name[index + 1:]
        return extension


class FileHandler:
    def __init__(self, path: str):
        self.__path = path
        self.__files = []

    def __iter__(self):
        self.n = 0
        return self 
    
    def __next__(self):
        if self.n < (len(self.__files)):
            file = self.__files[self.n]
            self.n += 1
            return file
        else:
            raise StopIteration
        
    @property
    def files(self):
        return self.__files

    def get_files(self):
        contents = os.listdir(self.__path)

        for file in contents:
            filepath = os.path.join(self.__path, file)
            if os.path.isfile(filepath):
                file_object = File(file, filepath)
                self.__files.append(file_object)


if __name__ == "__main__":
    path = "/Users/ntruong/Downloads/"
    file_handler = FileHandler(path)
    file_handler.get_files()

    for file in file_handler:
        print(file)