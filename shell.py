# shell.py
import tarfile
import os
from commands import Commands
from logger import Logger

class ShellEmulator:
    def __init__(self):
        self.current_directory = "/"
        self.logger = Logger("log.csv")

    def load_filesystem(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=self.current_directory)

    def execute(self, command):
        self.logger.log_command(command)
        cmd_parts = command.split()
        cmd_name = cmd_parts[0]

        if cmd_name == "ls":
            return Commands.ls(self.current_directory)
        elif cmd_name == "cd":
            if len(cmd_parts) > 1:
                return Commands.cd(cmd_parts[1])
            return "cd: missing argument"
        elif cmd_name == "exit":
            exit()
        elif cmd_name == "tail":
            if len(cmd_parts) > 1:
                return Commands.tail(cmd_parts[1])
            return "tail: missing file operand"
        elif cmd_name == "mv":
            if len(cmd_parts) == 3:
                return Commands.mv(cmd_parts[1], cmd_parts[2])
            return "mv: missing file operands"
        else:
            return f"{cmd_name}: command not found"
