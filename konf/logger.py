# logger.py
import csv
import os

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log_command(self, command):
        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([command])
