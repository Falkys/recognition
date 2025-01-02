line = "================================================================================================================="

from art import tprint
from Utils.commands import load_commands, get_command, get_patterns
from Utils.voice import callback, args, parser, sd, q
from vosk import Model, KaldiRecognizer
import sys
import json



commands = load_commands()
print(line)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model("./vosk/vosk")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        tprint('''
                                        Palladium
                                            by Falkys
        ''')
        print(line)
        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result()) 
                command = result.get("text", "")
                if not command:
                    continue
                print(line)
                print("")
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
                            sys.stdout.flush()
                        except Exception as e:
                            print(f"Ошибка выполнения команды: {e}")
                else:
                    print("Команда не найдена") 
            else:
                partial_result = json.loads(rec.PartialResult()) 
                text = partial_result.get("partial", "")
                if not text == "":
                    print(text)
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nЗавершение работы")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
    
    
# if __name__ == "__main__":
#     command = sys.stdin.read().strip()  # Чтение пути файла из stdin
#     print(f"[Recognizer] Вы сказали: {command}")
#     command_info = get_command(command, commands)
#     if command_info["info"]:
#         print(f"[Recognizer] Распознана комманда: {command_info["closest"]}")
#         print(line)
#         for info in command_info["info"]:
#             try:
#                 if info["isArrays"]:
#                     print(True)
#                     result1 = get_patterns(command_info)
#                     result = info["command"](result1)
#                 else:
#                     result = info["command"]()
#                 print(result)
#             except Exception as e:
#                 print(f"Ошибка выполнения команды: {e}")
#     else:
#         print("Команда не найдена")
