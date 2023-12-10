import re
from table2ascii import table2ascii as t2a, PresetStyle

SEND_MESSAGE_IF_NO_RESULTS = False

REGEX_WORDLE = re.compile("Wordle \d+ ([123456X])/6")
REGEX_TRADLE = re.compile("#Tradle #\d+ ([123456X])/6")
REGEX_ORDLIG = re.compile("ordlig.se nr \d+, ([123456X])/6")
REGEX_ORDEL = re.compile("Ordel #\d+ ([123456X])/6")

REGEX_ANY_SCORE = re.compile("((?:(^|\s))([123456X])([^0123456789]|$))|(((first)|(second)|(third)|(fourth)|(fifth)|(sixth))(\s|$))")

def get_statistics(message_data):
    result = {}
    for uid, name, msg in message_data:
        scores, scores_uncertain = parse_message(msg)
        if not scores and not scores_uncertain:
            continue

        if name not in result:
            result[name] = {}
        for game, score in scores.items():
            # We are confident about these ones, can overwrite if needed
            result[name][game] = score
        for game, score in scores_uncertain.items():
            # Only add these if we don't have any other data
            if not game in result[name]:
                result[name][game] = score

    return format_result(result)


def parse_message(msg):
    games_simple_regex = dict([
        ("Wordle", REGEX_WORDLE),
        ("Ordlig", REGEX_ORDLIG),
        ("Ordel", REGEX_ORDEL),
        ("Tradle", REGEX_TRADLE),
    ])

    results_certain = {}
    for line in msg.split("\n"):
        for game, game_regex in games_simple_regex.items():
            match = game_regex.search(line)
            if match:
                results_certain[game] = match.group(1)

    results_uncertain = {}
    try:
        results_uncertain = _find_uncertain_points(msg, games_simple_regex.keys())
    except Exception as e:
        print(f"Failed to parse message for uncertain points:\n{msg}\nError:\n{e}")

    return results_certain, results_uncertain

def _find_uncertain_points(msg, game_names):
    # Search your way forward grabbing games and points and put them together
    # as a hopeful wish. Assumes the game name always comes before the point,
    # so it will generate faulty information in cases like
    # 'I got a 4 on wordle and a 2 on tradle'
    # where tradle will have no data and wordle will be set to 2. Any other
    # more sophisticated methods would be appreciated here.
    results_uncertain = {}
    for line in msg.split("\n"):
        offset, game = _next_game(line, game_names)
        while game:
            next_game_offset, next_game = _next_game(line, game_names, offset+1)
            next_score_res = REGEX_ANY_SCORE.search(line[offset+1:], re.IGNORECASE)
            if not next_score_res:
                # No need looking for games, we don't have a score
                break
            if next_game and next_game_offset < offset + 1 + next_score_res.start():
                # This new game is before the points. Scrap the old game
                offset = next_game_offset
                game = next_game
                continue
            score = next_score_res.group()
            results_uncertain[game] = _prettify_score(score)
            offset = next_game_offset
            game = next_game
    return results_uncertain

def _prettify_score(score):
    score = score.strip()
    numbers_as_text = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6}
    if score[0].isdigit() or score[0].lower() == 'X':
        return score[0].upper()
    elif score in numbers_as_text.keys():
        return str(numbers_as_text[score])
    else:
        return score

def _next_game(haystack, needles, start=0):
    result_pos = -1
    result_needle = None
    for needle in needles:
        i = haystack.lower().find(needle.lower(), start)
        if i >= 0 and (result_pos == -1 or i < result_pos):
            result_pos = i
            result_needle = needle
    return result_pos, result_needle


def format_result(result):
    headers = ["Name", "Wordle", "Ordel", "Ordlig", "Tradle"]
    data = []
    for name, scores in result.items():
        shortened_name = name.split(" ")[0]  # TODO: Find a better way
        row = [shortened_name] + [scores.get(game, "-") for game in headers[1:]]
        data.append(row)

    if not result:
        if SEND_MESSAGE_IF_NO_RESULTS:
            text = "WOOT WOOT! Seems like today was no fun and games.\nLet's try again tomorrow!"
        else:
            text = None
    else:
        text = "WOOT WOOT! Statistics for todays games are:\n"
        text += t2a(header=headers, body=data, style=PresetStyle.thin_compact, cell_padding=0)
    return text
