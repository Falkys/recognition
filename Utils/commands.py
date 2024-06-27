import os
import importlib.util
import re
import difflib
import inspect

def get_patterns(command_info):
    template1 = find_value(command_info["closest"], command_info["info"][0]["names"])
    answer1 = command_info["closest"]
    result = extract_values(template1, answer1)
    return result

def find_value(key, array):
    for item in array:
        if key in item:
            return item[key]
    return None

def extract_values(template, answer):
    # Ищем все переменные в шаблоне вида { key: [val1, val2] }
    pattern = r'\{(\s*(\w+)\s*:\s*\[\s*([^\]]*)\s*\]\s*)\}'
    matches = re.findall(pattern, template)

    values = {}
    for match in matches:
        key = match[1].strip()
        options = [option.strip() for option in match[2].split(',')]

        # Строим регулярное выражение для поиска конкретного значения
        option_pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, options)))
        option_match = re.search(option_pattern, answer)
        if option_match:
            values[key] = option_match.group(0)

    return values

def isArray(name):
    pattern = r'\{[^:]+: \[(.*?)\]\}'
    match = re.search(pattern, name)
    
    if not match:
        return False
    else:
        return True

def combine(name):
    patterns = re.findall(r'\{[^}]+\}', name)

    # Заменяем шаблоны на их возможные комбинации
    combinations = [name]
    for pattern in patterns:
        options = re.findall(r'\[(.*?)\]', pattern)[0].split(', ')
        new_combinations = []
        for option in options:
            for comb in combinations:
                new_comb = comb.replace(pattern, option)
                new_combinations.append(new_comb)
        combinations = new_combinations
    
    return {"texts": combinations}

def load_commands():
    commands = []
    commands_folder = "./commands"

    for filename in os.listdir(commands_folder):
        if filename.endswith(".py"):
            filepath = os.path.join(commands_folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            command_info = { "names": [] }

            for name in module.names:
                arrays = isArray(name)
                if arrays:
                    command_info["isArrays"] = True
                    
                    result = combine(name)
                    for item in result['texts']:
                        command_info["names"].append({item: name})
                else:
                    names_1 = getattr(module, "names", [])
                    names = []
                    for name in names_1:
                        names.append({name: name})
                    command_info["names"] = names
                    command_info["isArrays"] = False

            command_info["sounds"] = getattr(module, "sounds", [])
            command_info["command"] = getattr(module, "main", None)
            command_info["takes_argument"] = len(inspect.signature(module.main).parameters) > 0

            commands.append(command_info)

    return commands

def get_command(command, commands):
    found_commands = { "info": [], "closest": '' }
    for command_info in commands:
        names = command_info["names"]
        name_0 = []
        for name_1 in names:
            key = list(name_1.keys())
            name_0.append(key[0])
        closest_matches = difflib.get_close_matches(command, name_0, n=1, cutoff=0.6)
        found_commands["input"] = command
        if closest_matches:
            closest_name = closest_matches[0]
            found_commands["closest"] = closest_name
            for name in name_0:
                if closest_name == name:
                    found_commands["info"].append(command_info)
                    break

    return found_commands