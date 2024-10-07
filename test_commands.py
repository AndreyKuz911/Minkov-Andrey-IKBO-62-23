import unittest
import os
import tempfile
import time
from commands import Commands

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "testfile.txt")
        self.source_file = os.path.join(self.test_dir.name, "source.txt")
        self.destination_file = os.path.join(self.test_dir.name, "destination.txt")
        
        with open(self.test_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

        with open(self.source_file, 'w') as f:
            f.write("This is a source file.")

    def tearDown(self):
        time.sleep(0.5)
        self.test_dir.cleanup()

    def test_ls(self):
        result = Commands.ls(self.test_dir.name)
        self.assertIn("testfile.txt", result)
        self.assertIn("source.txt", result)

    def test_cd(self):
        current_dir = os.getcwd()
        result = Commands.cd(self.test_dir.name)
        self.assertEqual(result, f"Changed directory to {self.test_dir.name}")
        self.assertEqual(os.getcwd(), self.test_dir.name)  # Проверяем, что директория изменилась
        os.chdir(current_dir)

    def test_tail(self):
        result = Commands.tail(self.test_file)
        self.assertEqual(result, "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

        # Проверка на файл с меньшим количеством строк
        short_file = os.path.join(self.test_dir.name, "shortfile.txt")
        with open(short_file, 'w') as f:
            f.write("Only one line.")
        result = Commands.tail(short_file)
        self.assertEqual(result, "Only one line.")

    def test_mv(self):
        result = Commands.mv(self.source_file, self.destination_file)
        self.assertEqual(result, f"Moved {self.source_file} to {self.destination_file}")
        self.assertFalse(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.destination_file))

        # Проверка на случай, если исходный файл не существует
        result = Commands.mv(self.source_file, self.destination_file)
        self.assertEqual(result, f"mv: {self.source_file}: No such file or directory")

if __name__ == "__main__":
    unittest.main()
