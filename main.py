line = "================================================================================================================="

from art import tprint
from Utils.commands import load_commands, get_command, get_patterns

commands = load_commands()
print(line)
tprint('''
                                Palladium
                                    by Falkys
''')
try:
    while True:
        print(line)
        print("")
        # сюда необработанная комманда
        command = input("[Recognizer] Команда: ").strip()
        print(f"[Recognizer] Вы сказали: {command}")
        command_info = get_command(command, commands)
        if command_info["info"]:
            print(f"[Recognizer] Распознана комманда: {command_info["closest"]}")
            print(line)
            for info in command_info["info"]:
                try:
                    if info["isArrays"]:
                        print(True)
                        result1 = get_patterns(command_info)
                        result = info["command"](result1)
                    else:
                        result = info["command"]()
                    print(result)
                except Exception as e:
                    print(f"Ошибка выполнения команды: {e}")
        else:
            print("Команда не найдена")
except KeyboardInterrupt:
    print("\nЗавершение работы")
