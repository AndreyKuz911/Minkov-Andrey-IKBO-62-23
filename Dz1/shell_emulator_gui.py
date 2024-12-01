import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from shell_emulator import ShellEmulator

# Убедимся, что Python находит модуль shell_emulator
sys.path.insert(0, os.path.dirname(__file__))

class EmulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Shell Emulator GUI")

        # Создание виджета для отображения вывода
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=20, width=80)
        self.output_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Поле для ввода команд
        self.command_entry = tk.Entry(master, width=80)
        self.command_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.command_entry.bind("<Return>", self.execute_command)  # Привязка нажатия Enter к выполнению команды
        self.command_entry.focus_set()  # Установка фокуса на поле ввода

        # Кнопка выхода из эмулятора
        self.exit_button = tk.Button(master, text="Выход", command=self.quit)
        self.exit_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Настройка строк и столбцов для изменения размера
        master.grid_rowconfigure(0, weight=1)  # Разрешаем текстовому полю менять размер
        master.grid_columnconfigure(0, weight=1)  # Разрешаем изменять размер по горизонтали

        # Инициализация эмулятора с тестовыми данными
        self.username = "user"
        self.zip_path = "Fs.zip"  # Путь к вашему ZIP файлу с файловой системой
        self.log_path = "log.html"
        
        try:
            self.emulator = ShellEmulator(self.username, self.zip_path, self.log_path)
            self.output_text.insert(tk.END, "Эмулятор запущен.\n")
            
            # Выводим содержимое текущей директории при запуске
            output_initial_ls = self.emulator.ls()
            self.output_text.insert(tk.END, output_initial_ls + "\n")
            
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка при загрузке эмулятора: {str(e)}\n")

    def execute_command(self, event=None):
        command = self.command_entry.get().strip()
        
        if command:
            output = self.emulator.execute_command(command)
            self.output_text.insert(tk.END, f"{self.username}@emulator:~$ {command}\n{output}\n")
            self.output_text.see(tk.END)  # Скроллим до последней строки
            self.command_entry.delete(0, tk.END)

    def quit(self):
        try:
            output_exit = self.emulator.execute_command("exit")
            self.output_text.insert(tk.END, f"{output_exit}\n")
            print(output_exit)  # Дополнительно выводим в консоль для отладки
            
            with open(self.emulator.log_path) as log_file:
                print(log_file.read())  # Выводим лог файл в консоль для проверки
            
            self.master.destroy()  # Закрываем окно
            
        except Exception as e:
            print(f"Ошибка при выходе: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorGUI(root)
    root.mainloop()