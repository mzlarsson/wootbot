import re
from table2ascii import table2ascii as t2a, PresetStyle

REGEX_WORDLE = re.compile("Wordle \d+ ([123456X])/6")
REGEX_TRADLE = re.compile("#Tradle #\d+ ([123456X])/6")
REGEX_ORDLIG = re.compile("ordlig.se nr \d+, ([123456X])/6")
REGEX_ORDEL = re.compile("Ordel #\d+ ([123456X])/6")

def get_statistics(message_data):
    result = {}
    for uid, name, msg in message_data:
        scores = parse_message(msg)
        if not scores:
            continue

        if name not in result:
            result[name] = {}
        for game, score in scores.items():
            result[name][game] = score

    return format_result(result)


def parse_message(msg):
    games_simple_regex = dict([
        ("Wordle", REGEX_WORDLE),
        ("Ordlig", REGEX_ORDLIG),
        ("Ordel", REGEX_ORDEL),
        ("Tradle", REGEX_TRADLE),
    ])

    results = {}
    for line in msg.split("\n"):
        for game, game_regex in games_simple_regex.items():
            match = game_regex.match(line)
            if match:
                results[game] = match.group(1)
    return results


def format_result(result):
    headers = ["Name", "Wordle", "Ordel", "Ordlig", "Tradle"]
    data = []
    for name, scores in result.items():
        row = [name] + [scores.get(game, "-") for game in headers[1:]]
        data.append(row)

    if not result:
        text = "WOOT WOOT! Seems like today was no fun and games.\nLet's try again tomorrow!"
    else:
        text = "WOOT WOOT! Statistics for todays games are:\n"
        text += t2a(header=headers, body=data, style=PresetStyle.thin_compact, cell_padding=0)
    return text
