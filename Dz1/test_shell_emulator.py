import os
import unittest
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Инициализация ShellEmulator с тестовыми параметрами."""
        self.username = "test_user"
        self.zip_path = "Fs.zip"
        
        if os.path.exists("log.html"):
            os.remove("log.html")

        self.emulator = ShellEmulator(self.username, self.zip_path, "log.html")

    def test_ls_command(self):
        result = self.emulator.ls()
        expected_files = ["file2.txt", "start.sh", "subdir1"]
        for expected in expected_files:
            self.assertIn(expected, result)

    def test_cd_command_valid(self):
        result = self.emulator.cd("subdir1")
        expected = '/Fs/subdir1'
        self.assertEqual(expected, self.emulator.current_directory)

    def test_cd_command_invalid(self):
        result = self.emulator.cd("invalid_directory")
        expected = "Директория 'invalid_directory' не найдена."
        self.assertEqual(expected, result)

    def test_exit_command(self):
        result = self.emulator.execute_command("exit")
        expected = "Выход из эмулятора."
        self.assertEqual(expected, result)

    def test_mv_command_valid(self):
        self.emulator.cd("subdir1")
        result = self.emulator.mv("file1.txt", "file1_moved.txt")
        expected = "Файл 'file1.txt' перемещен в 'file1_moved.txt'."
        self.assertIn(expected, result)

    def test_mv_command_invalid_source(self):
        result = self.emulator.mv("invalid_file.txt", "new_file.txt")
        expected = "Файл 'invalid_file.txt' не найден."
        self.assertEqual(expected, result)

    def test_mv_command_same_file(self):
        self.emulator.cd("subdir1")
        result = self.emulator.mv("file1.txt", "file1.txt")
        expected = "Файл 'file1.txt' перемещен в 'file1.txt'."
        self.assertIn(expected, result)

    def test_tail_command_subdir_file(self):
        """Проверка вывода последних строк файла в подкаталоге."""
        self.emulator.cd("subdir1")
        result = self.emulator.tail('file1.txt')
        expected = "apple\nbanana\napple\norange\nbanana\ngrape"
        self.assertEqual(result, expected)

    def test_tail_command_missing_file(self):
        """Проверка обработки ошибки при отсутствии файла."""
        result = self.emulator.tail('nonexistent.txt')
        expected = "Файл 'nonexistent.txt' не найден."
        self.assertEqual(result, expected)

    def test_tail_command_empty_file(self):
        """Проверка команды tail для пустого файла."""
        result = self.emulator.tail('empty.txt')
        expected = "Файл 'empty.txt' не найден."
        self.assertEqual(result, expected)

    def test_ls_command_subdir1(self):
        """Проверка команды ls для каталога subdir1, содержащего file1.txt."""
        self.emulator.cd("subdir1")
        result = self.emulator.ls()
        expected = "file1.txt (владелец: default_owner)"
        self.assertEqual(expected, result)

    def test_cd_command_back_and_forth(self):
        """Проверка перехода в подкаталог и возврата назад."""
        self.emulator.cd("subdir1")
        self.assertEqual('/Fs/subdir1', self.emulator.current_directory)
        
        self.emulator.cd("..")
        self.assertEqual('/Fs', self.emulator.current_directory)

if __name__ == '__main__':
    unittest.main()
