# Not all these functions are necessary but they permit to get some particular informations like the advanced stats about a particular match.

## FUNZIONI BASE

def competitions(area_code):
  url = base_url.format(f'/competitions?areaId={area_code}')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    competitions = response.json()
  else:
    print('error')

  return competitions
-------------------------------------------------------------------------------------------
def season(competitionwyId):
  url = base_url.format(f'/competitions/{competitionwyId}/seasons')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    season = response.json()['seasons']
  else:
    print('error')

  return season
-------------------------------------------------------------------------------------------
def get_team_stagione_corrente(competitionId): #you can't get old seasons
  url = base_url.format(f'/competitions/{competitionId}/teams')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    team = response.json()['teams']
  else:
    print('error')

  return team
-------------------------------------------------------------------------------------------
def get_team(seasonwyid): #you can get old seasons
  url = base_url.format(f'/seasons/{seasonwyid}/teams')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    team = response.json()['teams']
  else:
    print('error')

  return team
-------------------------------------------------------------------------------------------
def get_matches(team, season = ''):
  url = base_url.format(f'/teams/{team}/matches?seasonId={season}')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    matches = response.json()['matches']
  else:
    print('error')

  return matches
-------------------------------------------------------------------------------------------
def get_matches_detail(team,matchId):
  url = base_url.format(f'/matches/{matchId}')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    matches = response.json()
  else:
    print('error')

  return matches
-------------------------------------------------------------------------------------------
def get_events_per_match(matchId):
  url = base_url.format(f'/matches/{matchId}/events')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()['events']
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def team_squad(teamId):
  url = base_url.format(f'/teams/{teamId}/squad')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    squad = response.json()['squad']
  else:
    print('error')

  return squad
-------------------------------------------------------------------------------------------
def match_advanced_stats(team, matchId):
  url = base_url.format(f'/matches/{matchId}/advancedstats')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    match_stats = response.json()
  else:
    print('error')

  return match_stats
-------------------------------------------------------------------------------------------
def player_advanced_stats(playerId,competitionId):
  url = base_url.format(f'/players/{playerId}/advancedstats?compId={competitionId}')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()['total']
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def player_position(playerId,competitionId):
  url = base_url.format(f'/players/{playerId}/advancedstats?compId={competitionId}')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()['positions']
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def players_match_advanced_stats(playerId,matchId):
  url = base_url.format(f'/players/{playerId}/matches/{matchId}/advancedstats')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    players_match_advanced = response.json()['total']
  else:
    print('error')

  return players_match_advanced
-------------------------------------------------------------------------------------------
def teams_match_advanced_stats(teamId,matchId):
  url = base_url.format(f'/teams/{teamId}/matches/{matchId}/advancedstats')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def formazione(matchId):
  url = base_url.format(f'/matches/{matchId}/formations')

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def get_players_by_role(team_wyid = '', role_code2 = '', season_wyid = 188160):
  players = []

  url = base_url.format(f"/teams/{team_wyid}/squad?seasonId={season_wyid}")

  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    squad = response.json()['squad']
    for player in squad:
      if player['role']['code2'] == role_code2:
        players.append(player)
    return players
  else:
    print("errore")
    return -1
-------------------------------------------------------------------------------------------
def get_distance(start_x, start_y, end_x, end_y):
  starting_point = {'x': start_x, 'y': start_y}
  ending_point = {'x': end_x, 'y': end_y}
  third_point = {'x': start_x, 'y': end_y}
  starting_point_distance = np.absolute((starting_point['y']-third_point['y']))
  ending_point_distance = np.absolute((ending_point['x']-third_point['x']))
  start_end_distance = round(np.sqrt(pow(starting_point_distance, 2) + pow(ending_point_distance, 2)) , 2)
  return start_end_distance
-------------------------------------------------------------------------------------------
def season_teams(season):
  teams = []

  url = base_url.format(f"/seasons/{season}/teams")
  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()['teams']
  else:
    print('error')
    return -1
-------------------------------------------------------------------------------------------
def goal(team, season=''):
  goal = []
  for x in get_matches(team, season):
    for y in get_events_per_match(x['matchId']):
      if 'goal' in  y['type']['secondary'] and y['team']['id'] == team:
        goal.append(y)
  goal_totali = pd.DataFrame(goal)
  return goal_totali
-------------------------------------------------------------------------------------------
def season_detail(season):
  teams = []

  url = base_url.format(f"/seasons/{season}")
  response = requests.get(url, auth = HTTPBasicAuth(username, password))

  if response.ok:
    return response.json()['name']
  else:
    print('error')
    return -1
