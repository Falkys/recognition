import re

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

# Пример использования:
template1 = "звук на { info: [один, два]} {mds: [да, нет]}"
answer1 = 'звук на один да'

result1 = extract_values(template1, answer1)
print(result1)  # Ожидаемый вывод: {'info': 'один', 'mds': 'да'}

template2 = "ты {bam: [хуй, не хуй]} человек {ban: [бро, братан]}"
answer2 = 'ты не хуй человек братан'

result2 = extract_values(template2, answer2)
print(result2)  # Ожидаемый вывод: {'bam': 'не хуй', 'ban': 'братан'}
