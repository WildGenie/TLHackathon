import hashlib
import data
import json

def hash(*argv):
    hash_key = ''.join(str(arg) for arg in argv)
    return hashlib.md5(hash_key.encode()).hexdigest()


champions = data.load_champions()
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

champions_custom = data.load_champions_custom()
def get_ids_to_custom():
    name_to_id = {
        champion: int(champions[champion]['key']) for champion in champions
    }

    return {
        name_to_id[champion['Champion'].replace(' ', '')]: champion
        for champion in champions_custom
    }

def get_primaries():
    primaries = {champion['Primary'] for champion in champions_custom}
    return list(primaries)



def convert_names_to_ids(names):
    name_to_id = {
        champion: int(champions[champion]['key']) for champion in champions
    }

    ids = [str(name_to_id[name]) for name in names]
    print(','.join(ids))

convert_names_to_ids([ 'Janna', 'Sona', 'Lulu', 'Soraka', 'Nami' ])