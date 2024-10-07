# gui.py
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from shell import ShellEmulator

class ShellGUI:
    def __init__(self, master):
        self.master = master
        master.title("Shell Emulator")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

        self.command_entry = tk.Entry(master)
        self.command_entry.pack(fill=tk.X)
        self.command_entry.bind("<Return>", self.execute_command)

        self.emulator = ShellEmulator()

    def execute_command(self, event):
        command = self.command_entry.get()
        output = self.emulator.execute(command)
        self.text_area.insert(tk.END, f"$ {command}\n{output}\n")
        self.command_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShellGUI(root)
    root.mainloop()
