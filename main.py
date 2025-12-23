import os
import shutil
from datetime import datetime

class FileOperations: # главный модуль для копирования
    
    @staticmethod
    def copy_file(source, destination, overwrite=True, preserve_metadata=True):
        # если выбран режим одиночного копирования файлов
        if not os.path.exists(source):
            raise FileNotFoundError(f"Файл не существует: {source}")
        
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
        
        filename = os.path.basename(source)
        dest_file = os.path.join(destination, filename)
        
        # проверка на существования файла
        if os.path.exists(dest_file) and not overwrite:
            # генерация уникального имени если уже существует файл и выключена опция перезаписки
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(destination, f"{name}_{counter}{ext}")):
                counter += 1
            dest_file = os.path.join(destination, f"{name}_{counter}{ext}")
            filename = f"{name}_{counter}{ext}"
        
        # выбор функции копирования
        copy_func = shutil.copy2 if preserve_metadata else shutil.copy
        copy_func(source, dest_file)
        
        return dest_file, filename
    
    @staticmethod
    def copy_directory(source, destination, overwrite=True, preserve_metadata=True):
        # копирование директории если выбран режим копирования нескольких файлов
        if not os.path.exists(source):
            raise FileNotFoundError(f"Директория не существует: {source}")
        
        if not os.path.isdir(source):
            raise ValueError(f"Источник не является директорией: {source}")
        
        folder_name = os.path.basename(source)
        dest_folder = os.path.join(destination, folder_name)
        
        # проверка существования директории
        if os.path.exists(dest_folder) and not overwrite:
            counter = 1
            while os.path.exists(f"{dest_folder}_{counter}"):
                counter += 1
            dest_folder = f"{dest_folder}_{counter}"
            folder_name = f"{folder_name}_{counter}"
        
        # копирование папки с содержимым
        copy_func = shutil.copy2 if preserve_metadata else shutil.copy
        shutil.copytree(source, dest_folder, copy_function=copy_func)
        
        # Подсчет скопированных файлов
        file_count = sum([len(files) for _, _, files in os.walk(dest_folder)])
        
        return dest_folder, folder_name, file_count
    
    @staticmethod
    def get_file_info(filepath): # информация о файле если копируем с метаданными
        if not os.path.exists(filepath):
            return {"error": "Файл не существует"}
        
        info = {
            "filename": os.path.basename(filepath),
            "path": filepath,
            "size": os.path.getsize(filepath),
            "modified": datetime.fromtimestamp(os.path.getmtime(filepath)),
            "created": datetime.fromtimestamp(os.path.getctime(filepath)),
            "is_dir": os.path.isdir(filepath),
            "extension": os.path.splitext(filepath)[1] if os.path.isfile(filepath) else ""
        }
        
        if info["is_dir"]:
            info["file_count"] = sum([len(files) for _, _, files in os.walk(filepath)])
        
        return info
    
    @staticmethod
    def format_size(size_bytes): # форматирование размера
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

def main(): # запуск программы
    import tkinter as tk
    from guiModule import FileCopyApp
    
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()