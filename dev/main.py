import os
from datetime import datetime 

class File:
    def __init__(self, name: str, path: str):
        self.__name = name 
        self.__path = path
        self.__directory = self.get_directory()
        self.__date = self.get_date()
        self.__extension = self.get_extension()

    def __str__(self):
        return f"Filename: {self.__name} \nFilepath: {self.__path}\nDirectory: {self.__directory}\nCreation date: {self.__date}\nExtension: {self.__extension}\n"

    @property
    def name(self):
        return self.__name 
    
    @property
    def path(self):
        return self.__path
    
    @property 
    def date(self):
        return self.__date
    
    @property
    def extension(self):
        return self.__extension
    
    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    def get_date(self):
        unix_date = int(os.stat(self.__path).st_birthtime)
        date = datetime.utcfromtimestamp(unix_date).strftime("%y%m%d")
        return date
    
    def get_directory(self):
        index = self.__path.rfind("/")
        directory = self.__path[:index + 1]
        return directory
    
    def get_extension(self):
        index = self.__name.rfind(".")
        extension = self.__name[index + 1:]
        return extension
    
    def add_date_to_filename(self):
        old_file = self.__path
        new_file = self.__directory + self.__date + "_" + self.__name
        length = len(self.__date)

        if not self.__name[:length].isdigit():
            os.rename(old_file, new_file)
        else:
            print("Filename already contains the date in YYMMDD-format. Nothing was changed.")

    def move_to(self, folder_type: str):
        types = {"extension": self.__extension, "date": self.__date[:4]}
        old_path = self.__path 
        new_path = self.__directory + types[folder_type]
        new_path_with_file = self.__directory + types[folder_type] + "/" + self.__name

        if os.path.isdir(new_path):
            os.replace(old_path, new_path_with_file)


class FileHandler:
    def __init__(self, path: str):
        self.__path = path
        self.__files = self.get_files()
        ignored_extensions = ["DS_Store", "localized"]
        self.__extensions = {file.extension for file in self.__files if file.extension not in ignored_extensions}
        self.__dates = {file.date[:4] for file in self.__files}

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
        files = []

        for file in contents:
            filepath = os.path.join(self.__path, file)
            if os.path.isfile(filepath):
                file_object = File(file, filepath)
                files.append(file_object)

        return files

    def create_folders(self, type: str):
        types = {"extension": self.__extensions, "date": self.__dates}

        for folder_name in types[type]:
            new_path = self.__path + folder_name
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                print(f"Yeah, I created the folder '{new_path}', sir.")
            else:
                print(f"Sorry, the folder '{new_path}' already exists.")

    def move_files_to(self, folder_type: str):
        for file in self.__files:
            file.move_to(folder_type)

    def add_date_to_filenames(self):
        for file in self.__files:
            file.add_date_to_filename()


if __name__ == "__main__":
    path = "/Users/ntruong/Downloads/"
    file_handler = FileHandler(path)
    file_handler.create_folders("date")
    file_handler.move_files_to("date")


# TODO:
# - If a file has already a date at the beginning replace it with "YYMMDD_"
# - Reformat description of a file to CamelCase