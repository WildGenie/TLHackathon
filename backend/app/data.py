import os
import json

champions_data_path = os.path.join(os.path.dirname(__file__), './data/champions.json')
champions_custom_data_path = os.path.join(os.path.dirname(__file__), './data/champions_custom.json')

# ------------------------------ Champions data ------------------------------
def load_champions():
    return json.load(open(champions_data_path, 'r'))['data']

def load_champions_custom():
    return json.load(open(champions_custom_data_path, 'r'))

champions = load_champions()
champions_custom = load_champions_custom()

def get_champion_to_tags():
    return {
        int(champions[champion]['key']): champions[champion]['tags']
        for champion in champions
    }


def get_tags():
    tags = set()
    for champion in champions:
        for tag in champions[champion]['tags']:
            tags.add(tag)
    return list(tags)

def get_ids_to_custom():
    name_to_id = {
        champion: int(champions[champion]['key']) for champion in champions
    }

    return {
        name_to_id[champion['Champion'].replace(' ', '')]: champion
        for champion in champions_custom
    }