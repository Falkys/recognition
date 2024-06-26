import re

# Используем регулярное выражение для нахождения всех шаблонов `{ ... }`
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
    
    return combinations
name = "звук на { info: [один, два]} { mds: [да, нет, ША]}"
print(combine(name))

