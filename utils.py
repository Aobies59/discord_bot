import time
from global_variables import LOGS_FOLDERNAME, LOGFILES_TO_KEEP, COMMAND_SIZE
import threading
import os

logs_file_lock = threading.Lock()
logs_filename = ''

def clean_logs():
    global logs_filename
    for log_file in os.listdir(LOGS_FOLDERNAME):
        log_file_full_name = f'{LOGS_FOLDERNAME}/{log_file}'
        if log_file_full_name == logs_filename or log_file in LOGFILES_TO_KEEP:
            continue
        else:
            try:
                os.remove(log_file_full_name)
            except PermissionError:
                continue

def init_logs():
    global logs_filename
    logs_filename = f'{LOGS_FOLDERNAME}/{time.strftime("%Y-%m-%d|%H:%M:%S", time.localtime())}.txt'
    with logs_file_lock:
        logs_file = open(logs_filename, "w")
        logs_file.close()

def log(message):
    global logs_filename
    if logs_filename == '':
        init_logs()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with logs_file_lock:
        with open(logs_filename, "a") as logs_file:
            logs_file.write(f"{timestamp} - {message}\n")

def divide_string_by_first_space(string_to_divide: str) -> (str, str):
    division_index: int = string_to_divide.find(" ")
    part_1: str = string_to_divide
    part_2: str = ""

    if division_index != -1:
        part_1 = string_to_divide[:division_index].strip()
        part_2 = string_to_divide[division_index:].strip()
    return part_1, part_2

def equalize_len(command: str):
    beautified_command = command
    while len(beautified_command) < COMMAND_SIZE:
        beautified_command += ' '
    return beautified_command
