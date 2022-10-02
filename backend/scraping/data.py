import atexit
import json
import os

MATCH_DATA_NUM = 83

challenger_data_path = os.path.join(os.path.dirname(__file__), './data/challenger.json')
champions_data_path = os.path.join(os.path.dirname(__file__), './data/champions.json')
champions_custom_data_path = os.path.join(os.path.dirname(__file__), './data/champions_custom.json')
match_data_path = os.path.join(
    os.path.dirname(__file__),
    f'./data/match_data/matches_{MATCH_DATA_NUM}.json',
)

extended_match_data_path = os.path.join(
    os.path.dirname(__file__),
    f'./data/extended_match_data/extended_matches_{MATCH_DATA_NUM}.json',
)

parsed_matches_path = os.path.join(os.path.dirname(__file__), './data/parsed_matches.csv')

# ------------------------------ champions data ------------------------------
def load_champions():
    return json.load(open(champions_data_path, 'r'))['data']

def load_champions_custom():
    return json.load(open(champions_custom_data_path, 'r'))

# ------------------------------ challenger data ------------------------------
def load_challenger():
    challenger = json.load(open(challenger_data_path, 'r'))
    return challenger['entries']


# ------------------------------ match data ------------------------------
def load_matches():
    return json.load(open(match_data_path, 'r'))


def save_matches(new_matches_list):
    print(f'saving {len(new_matches_list)} matches')
    with open(match_data_path, 'w') as f:
        json.dump(new_matches_list, f)


def add_matches(new_matches_list):
    current_matches = load_matches()
    union = list(set(current_matches) | set(new_matches_list))
    print(len(union))
    save_matches(union)


# ------------------------------ extended match data ------------------------------
def load_extended_matches():
    try:
        return json.load(open(extended_match_data_path, 'r'))
    except:
        return {}


def save_extended_matches(new_matches_map):
    # print('saving {} matches'.format(len(new_matches_map)))
    with open(extended_match_data_path, 'w') as f:
        json.dump(new_matches_map, f)


# ------------------------------ parsed match data ------------------------------
def save_callapsed_data(parsed_matches_list):
    print(f'saving {len(parsed_matches_list)} matches')
    with open(parsed_matches_path, 'w') as f:
        for parsed_match in parsed_matches_list:
            f.write("{}{}".format(parsed_match, '\n'))