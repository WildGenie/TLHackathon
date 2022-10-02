from keras.models import load_model
import json
import os
import data
import roleidentification

model_5v5 = os.path.join(os.path.dirname(__file__), './data/model_5v5.h5')
model_5v5_loaded = load_model(model_5v5, compile=True)

champion_roles = roleidentification.pull_data()
champion_id_to_custom = data.get_ids_to_custom()

BLANK_PRIMARIES = {
                'Skirmisher' : 0,
                'Juggernaut' : 0,
                'Battlemage' : 0,
                'Enchanter'  : 0,
                'Catcher'    : 0,
                'Artillery'  : 0,
                'Burst'      : 0,
                'Diver'      : 0,
                'Warden'     : 0,
                'Assassin'   : 0,
                'Marksman'   : 0,
                'Vanguard'   : 0,
                'Specialist' : 0
            }

def flatten_champion(champion_id):
    champion_custom = champion_id_to_custom[champion_id]
    return [
        champion_custom['Damage'],
        champion_custom['Toughness'],
        champion_custom['Control'],
        champion_custom['Mobility'],
        champion_custom['Utility'],
        champion_custom['Damage Type'],
    ]


def order_team(tag_mapping, role_mapping):
    ordered_list = []
    ordered_list.extend(flatten_champion(role_mapping['TOP']))
    ordered_list.extend(flatten_champion(role_mapping['JUNGLE']))
    ordered_list.extend(flatten_champion(role_mapping['MIDDLE']))
    ordered_list.extend(flatten_champion(role_mapping['BOTTOM']))
    ordered_list.extend(flatten_champion(role_mapping['UTILITY']))
    ordered_list.extend(
        (
            tag_mapping['Skirmisher'],
            tag_mapping['Juggernaut'],
            tag_mapping['Battlemage'],
            tag_mapping['Enchanter'],
            tag_mapping['Catcher'],
            tag_mapping['Artillery'],
            tag_mapping['Burst'],
            tag_mapping['Diver'],
            tag_mapping['Warden'],
            tag_mapping['Assassin'],
            tag_mapping['Marksman'],
            tag_mapping['Vanguard'],
            tag_mapping['Specialist'],
        )
    )

    return ordered_list

def calculate_team_primaries(team):
    ids_to_custom = data.get_ids_to_custom()

    primaries = BLANK_PRIMARIES.copy()
    for champion_id in team:
        primary = ids_to_custom[champion_id]['Primary']
        primaries[primary] += 1
    return primaries

def calculate_win_team_1_chance(team_1, team_2):
    team_1_tags = calculate_team_primaries(team_1)
    team_2_tags = calculate_team_primaries(team_2)

    team_1_roles = roleidentification.get_roles(champion_roles, team_1)
    team_2_roles = roleidentification.get_roles(champion_roles, team_2)

    team_1_parsed = order_team(team_1_tags, team_1_roles)
    team_2_parsed = order_team(team_2_tags, team_2_roles)

    prediction1 = model_5v5_loaded.predict_proba( [team_1_parsed + team_2_parsed] )[0][0]
    prediction2 = 1 - model_5v5_loaded.predict_proba( [team_2_parsed + team_1_parsed] )[0][0]
    prediction = (prediction1 + prediction2) / 2

    return int(prediction * 100)
