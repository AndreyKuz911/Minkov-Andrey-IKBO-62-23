import os

class Commands:
    @staticmethod
    def ls(current_directory):
        """Список файлов и папок в текущей директории."""
        try:
            return "\n".join(os.listdir(current_directory))
        except FileNotFoundError:
            return "ls: no such file or directory"

    @staticmethod
    def cd(directory):
        """Изменить текущую директорию."""
        try:
            os.chdir(directory)
            return f"Changed directory to {directory}"
        except FileNotFoundError:
            return f"cd: no such file or directory: {directory}"
        except PermissionError:
            return f"cd: permission denied: {directory}"

    @staticmethod
    def tail(filename, lines=10):
        """Показать последние строки файла."""
        try:
            with open(filename, 'r') as file:
                return ''.join(file.readlines()[-lines:])
        except FileNotFoundError:
            return f"tail: {filename}: No such file"
        except Exception as e:
            return f"tail: {filename}: {str(e)}"

    @staticmethod
    def mv(source, destination):
        """Переместить файл из источника в назначение."""
        try:
            if not os.path.exists(source):
                return f"mv: {source}: No such file or directory"
            os.rename(source, destination)
            return f"Moved {source} to {destination}"
        except FileNotFoundError:
            return f"mv: {source}: No such file or directory"
        except PermissionError:
            return f"mv: {source}: permission denied"
        except Exception as e:
            return f"mv: {str(e)}"
