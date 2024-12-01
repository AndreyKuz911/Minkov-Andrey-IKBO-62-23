import sys
from shell_emulator import ShellEmulator

def main():
    if len(sys.argv) < 2:
        print("Использование: python startup_script.py <commands_file>")
        sys.exit(1)
    
    commands_file = sys.argv[1]
    
    # Инициализация эмулятора с необходимыми путями
    username = 'test_user'
    zip_path = 'Fs.zip'   # Убедитесь, что этот ZIP-файл существует и содержит вашу файловую систему
    log_path = 'log.html'
    
    emulator = ShellEmulator(username, zip_path, log_path)
    
    try:
        with open(commands_file, 'r', encoding='utf-8') as f:
            commands = f.readlines()
        
        for command in commands:
            command = command.strip()
            
            # Игнорирование пустых строк и строк-комментариев
            if not command or command.startswith('#'):
                continue
            
            print(f"> {command}")
            output = emulator.execute_command(command)
            print(output)
            
            if command.lower() == 'exit':
                print("Эмулятор завершил работу.")
                break
            
    except FileNotFoundError:
        print(f"Файл с командами '{commands_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении команд: {str(e)}")

if __name__ == '__main__':
    main()
