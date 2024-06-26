"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape the app ids given a user's profile id.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests


def scrape_app_ids(profile_id: int, n: int) -> list[int]:
    """Returns a list of the user's n most played games (in minutes).
    Return an empty list if the user has hidden game details.
    If the user has less than n games, return all the games they have.

    Preconditions:
        - len(profile_id) == 17
        - n > 0

    >>> scrape_app_ids('star_19642', 2)
    [252950, 1172470]
    >>> scrape_app_ids(76561199000093113, 2)
    [252950, 1172470]
    """
    params = {
        'key': '<Your Steam Web API Key>', # You can request for a key at https://steamcommunity.com/dev/apikey
        'steamid': str(profile_id),
        'format': 'json'
    }
    json_response = get_json_response(params)

    if not json_response:
        return []

    games = json_response['games']
    games_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)

    if len(games_by_playtime) < n:
        return [game['appid'] for game in games_by_playtime]
    else:
        return [games_by_playtime[i]['appid'] for i in range(n)]


def get_json_response(params: dict) -> requests.models.Response.json:
    """Helper function for scrape_app_ids().
    Returns the JSON response of the games list page given params.

    Preconditions:
        - 'key' in params
        - 'steamid' in params and len(params['steamid']) == 17
        - params['format'] == 'json'
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    response = requests.get(url, params)
    return response.json()['response']


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['requests'],
        'allowed-io': [],
        'max-line-length': 120
    })
