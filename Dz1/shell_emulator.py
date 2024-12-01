import os
import zipfile
from datetime import datetime
import html

class ShellEmulator:
    def __init__(self, username, zip_path, log_path):
        self.username = username
        self.zip_path = zip_path
        self.log_path = log_path
        self.current_directory = '/Fs'  # Инициализация корневого каталога
        self.filesystem = self.load_filesystem(zip_path)  # Загрузка файловой системы

    def load_filesystem(self, zip_path):
        """Загрузить файловую систему из ZIP-файла."""
        filesystem = {}
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                parts = file_name.split('/')
                current_level = filesystem

                for part in parts[:-1]:  # Создание структуры каталогов в файловой системе
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

                if parts[-1]:  # Если это не каталог
                    try:
                        content = zip_ref.read(file_name).decode('utf-8')
                    except UnicodeDecodeError:
                        content = zip_ref.read(file_name).decode('utf-8', errors='ignore')
                    current_level[parts[-1]] = {
                        'content': content,
                        'owner': 'default_owner'  # Убедитесь, что этот ключ присутствует
                    }
        return filesystem

    def log_command(self, command):
        """Записывает команду в лог-файл в формате HTML."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_dir = self.current_directory
        with open(self.log_path, mode='a') as log_file:
            log_file.write(f"<p>{html.escape(self.username)}: {html.escape(command)} в {html.escape(current_dir)} - {timestamp}</p>\n")

    def execute_command(self, command):
        """Выполняет команду и возвращает результат."""
        self.log_command(command)
        parts = command.split()
        
        if not parts:
            return "Пустая команда."

        cmd = parts[0]
        
        try:
            if cmd == 'ls':
                return self.ls()
            elif cmd == 'cd':
                return self.cd(parts[1] if len(parts) > 1 else '')
            elif cmd == 'mv':
                return self.mv(parts[1], parts[2]) if len(parts) == 3 else "Использование: mv <source> <destination>"
            elif cmd == 'tail':
                return self.tail(parts[1]) if len(parts) > 1 else "Использование: tail <file>"
            elif cmd == 'exit':
                return "Выход из эмулятора."
            
            return f"Команда '{cmd}' не поддерживается."
        
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def ls(self):
        """Выводит список файлов и директорий в текущем каталоге."""
        current_level = self.get_current_directory()
        if current_level:
            output = []
            for item, properties in current_level.items():
                owner = properties.get('owner', 'неизвестный владелец')  # Используйте get для безопасного доступа
                output.append(f"{item} (владелец: {owner})")
            return '\n'.join(output)
        
        return "Директория не найдена."

    def cd(self, path):
        """Сменяет текущую директорию или выводит текущую директорию, если путь не указан."""
        if not path:
            return f"{self.current_directory}"

        if path == "..":
            if self.current_directory != '/Fs':
                parts = self.current_directory.strip('/').split('/')
                parts.pop()  # Удаляем последний элемент (каталог)
                if parts:
                    self.current_directory = '/' + '/'.join(parts)
                else:
                    self.current_directory = '/Fs'
            return ""

        target = path.strip('/')

        current_level = self.get_current_directory()

        if target in current_level:
            self.current_directory += '/' + target if not target.startswith('/') else target  
            return f"Сменена директория на: {self.current_directory}"
        
        return f"Директория '{path}' не найдена."


    def mv(self, source_file, destination_file):
        """Перемещает файл из source_file в destination_file."""
        current_level = self.get_current_directory()
        
        if source_file in current_level:
            current_level[destination_file] = current_level.pop(source_file)
            return f"Файл '{source_file}' перемещен в '{destination_file}'."
        
        return f"Файл '{source_file}' не найден."

    def tail(self, file_name):
        """Выводит последние 10 строк указанного файла."""
        current_level = self.get_current_directory()
        if not current_level or file_name not in current_level:
            return f"Файл '{file_name}' не найден."
        
        file_content = current_level[file_name].get('content')
        if file_content is None or file_content.strip() == "":
            return f"Файл '{file_name}' пуст или недоступен."
        
        # Разбиваем содержимое файла на строки и берем последние 10
        lines = file_content.splitlines()[-10:]
        return '\n'.join(lines)


    def get_current_directory(self):
       """Возвращает содержимое текущей директории."""
       current_level=self.filesystem
        
       for part in self.current_directory.strip('/').split('/'):
           if part:
               current_level=current_level.get(part)
               if current_level is None:
                   return None
        
       return current_level


# Пример использования (для тестирования)
if __name__ == '__main__':
    username='test_user'
    zip_path='Fs.zip'
    log_path='log.html'

    emulator=ShellEmulator(username,zip_path,log_path)
    
    while True:
       command=input(f"{username}@emulator:~$ ")
       
       output=emulator.execute_command(command)
       print(output)
       
       if command=='exit':
           break