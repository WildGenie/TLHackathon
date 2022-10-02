import json
import math
import requests
import urllib
from ratelimit import limits
from cachetools import cached, TTLCache

from config import RIOT_HOST, RIOT_API_KEY, NUM_MATCHES
from data import add_matches, load_extended_matches, save_extended_matches
from util import hash


# ------------------------------ Request Handler ------------------------------
riot_session = requests.Session()


@limits(calls=2, period=3)
def make_call(url, headers):
	return riot_session.get(url, headers=headers)

@cached(cache=TTLCache(maxsize=1024, ttl=600), key=hash)
def riot_request(endpoint, params={}):

	url = f'{RIOT_HOST}/{endpoint}?{urllib.parse.urlencode(params)}'
	print(url)

	headers = {
		'X-Riot-Token' : RIOT_API_KEY
	}

	r = None
	while r is None:
		try:
			r = make_call(url, headers)
		except:
			pass

	if r.status_code != 200:
		raise Exception(
			f'Failed to make request to Riot\nStatus Code: {r.status_code}'
		)


	return r.json()


# ------------------------------ Data Collection ------------------------------
def get_account_id(player_name):
	endpoint = f'lol/summoner/v4/summoners/by-name/{player_name}'
	account_data = riot_request(endpoint)
	return account_data['accountId']


def get_account_matches(player_id, num_matches=100):
	endpoint = f'lol/match/v4/matchlists/by-account/{player_id}'

	matches = []
	for i in range(math.ceil(num_matches/100)):
		match_data = riot_request(endpoint, { "beginIndex" : i * 100 } )

		matches.extend(match['gameId'] for match in match_data['matches'])
	return matches


def get_match_details(match_id):

	endpoint = f'lol/match/v4/matches/{match_id}'
	return riot_request(endpoint)

# ------------------------------ Data Manipulation ------------------------------
def get_match_history(player_name):
	account_id = get_account_id(player_name)
	return get_account_matches(account_id, NUM_MATCHES)


def get_tons_of_matches(player_names):
	match_ids = set()
	for player_name in player_names:
		player_matches = get_match_history(player_name)
		match_ids.update(player_matches)
		match_id_list = list(match_ids)
		add_matches(match_id_list)
	return list(match_ids)

def get_expanded_matches(match_id_list):
	expanded_matches = load_extended_matches()
	for match_id in match_id_list:
		print(f"{len(expanded_matches)} matches recorded")
		if str(match_id) in expanded_matches:
			continue
		match_details = get_match_details(match_id)
		expanded_matches[match_id] = match_details
		save_extended_matches(expanded_matches)

	return expanded_matches
        

