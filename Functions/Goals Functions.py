These functions permit to identify 10 different type of goals.
All of them return a dataframe with all goals and shots, the number of shots (including goals) and the number of goals itself.

## GOALS

def get_penalty(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  shots = 0
  goal = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'penalty' and e['team_id'] == team_wyid:
        e['shotType'] = 'PenaltyKick'
        shot.append(e)
    shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal
-------------------------------------------------------------------------------
def get_free_kick_shot(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  shots = 0
  goals = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'free_kick' and 'free_kick_shot' in e['secondary'] and e['team_id'] == team_wyid:
        e['shotType'] = 'DirectFreeKick'
        shot.append(e)
  shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goals += 1
    else:
      shots += 1
  return shots_df, shots, goals

-------------------------------------------------------------------------------
def get_indirect_free_kick_shot(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  goal = 0
  shots = 0
  first_free_kick = 0
  j = 0
  z = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & (eventi_df.primary != 'interception')]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'shot' and e ['team_id'] == team_wyid:
        first_free_kick = ((eventi_df.loc[i::-1, 'primary'].eq('free_kick')) & (eventi_df.loc[i::-1, 'team_id'].eq(team_wyid))).idxmax()
        if i-first_free_kick != 0:
          if 'free_kick_cross' in eventi_df.loc[i-1, 'secondary']:
              e['shotType'] = 'IndirectFreeKickWithCross'
              shot.append(e)
          elif 'free_kick_cross' in eventi_df.loc[i-2, 'secondary'] and (eventi_df.loc[i-1,'primary'] == 'pass' and 'head_pass' in eventi_df.loc[i-1, 'secondary']):
              e['shotType'] = 'IndirectFreeKickWithCrossAndHeadBank'
              shot.append(e)
          elif 'free_kick_cross' in eventi_df.loc[i-2, 'secondary'] and (eventi_df.loc[i-1,'primary'] == 'pass' and 'head_pass' not in eventi_df.loc[i-1, 'secondary']):
              e['shotType'] = 'IndirectFreeKickWithCrossAndBank'
              shot.append(e)
          elif eventi_df.loc[i-2, 'primary'] == 'free_kick' and 'free_kick_shot' not in eventi_df.loc[i-2, 'secondary'] and get_distance(eventi_df.loc[i-2, 'location']['x'],\
               eventi_df.loc[i-2, 'location']['y'], eventi_df.loc[i-2, 'pass']['endLocation']['x'], eventi_df.loc[i-2, 'pass']['endLocation']['y']) < 3:
              if eventi_df.loc[i-1, 'primary'] == 'pass' and 'cross' in eventi_df.loc[i-1, 'secondary']:
                e['shotType'] = 'IndirectFreeKickWithTouchAndCross'
                shot.append(e)
              elif eventi_df.loc[i-1, 'primary'] == 'touch':
                e['shotType'] = 'IndirectFreeKickWithTwoTouches'
                shot.append(e)
              elif eventi_df.loc[i-1, 'primary'] == 'pass':
                e['shotType'] = 'IndirectFreeKickWithTouchAndPass'
                shot.append(e)
          elif eventi_df.loc[i-1, 'primary'] == 'free_kick' and 'free_kick_shot' not in eventi_df.loc[i-1, 'secondary'] and get_distance(eventi_df.loc[i-1, 'location']['x'],\
               eventi_df.loc[i-1, 'location']['y'], eventi_df.loc[i-1, 'pass']['endLocation']['x'], eventi_df.loc[i-1, 'pass']['endLocation']['y']) < 3:
              e['shotType'] = 'IndirectFreeKickWithTouch'
              shot.append(e)
          elif i-first_free_kick <=4 and i-first_free_kick != 1:
            for x in range(i, first_free_kick-1, -1):
              if eventi_df.loc[x, 'primary'] == 'touch':
                z += 1
            if z == 1:
              e['shotType'] = 'IndirectFreeKickWithCrossAndBounce'
              shot.append(e)
            elif z == 2:
              e['shotType'] = 'IndirectFreeKickWithCrossAndTwoBounces'
              shot.append(e)
            elif z == 3:
              e['shotType'] = 'IndirectFreeKickWithCrossAndThreeBounces'
              shot.append(e)
            elif z == 4:
              e['shotType'] = 'IndirectFreeKickWithCrossAndFourBounces'
              shot.append(e)
  shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal
-------------------------------------------------------------------------------
def get_throw_in_shot(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  goal = 0
  shots = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & (eventi_df.primary != 'interception') & ('loss' not in eventi_df.secondary)]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'shot' and e['team_id'] == team_wyid:
        first_throw_in = (eventi_df.loc[i::-1, 'primary'].eq('throw_in') & eventi_df.loc[i::-1, 'team_id'].eq(team_wyid)).idxmax()
        if i- first_throw_in == 0:
          break
        elif i - first_throw_in <= 7:
          j = True
          for x in range(i, first_throw_in, -1):
              if eventi_df.loc[x, 'primary'] == 'free_kick' or eventi_df.loc[x, 'primary'] == 'corner':
                j = False
                break
          if j:
            e['shotType'] = 'shotAfterThrowIn'
            shot.append(e)

  shots_df = pd.DataFrame(shot)
  for x, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal

-------------------------------------------------------------------------------
def get_ball_recovery(team_wyid, season_wyid = ''):
  shot = []
  goal = 0
  shots_df = pd.DataFrame(shot)
  shots = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & ('loss' not in eventi_df.secondary)]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'shot' and e ['team_id'] == team_wyid and 'shot_after_free_kick' not in e['secondary']:
        last_opponent = (eventi_df.loc[i::-1, 'team_id'] != team_wyid).idxmax()
        if i- last_opponent <= 7:
          j = True
          for x in range(i, last_opponent, -1):
            if eventi_df.loc[x, 'primary'] == 'throw_in' or eventi_df.loc[x, 'primary'] == 'free_kick' or eventi_df.loc[x, 'primary'] == 'corner':
              j = False
              break

          if j:
            if eventi_df.loc[last_opponent+1, 'location']['x'] < 66:
              if eventi_df.loc[i, 'location']['x'] - eventi_df.loc[last_opponent+1, 'location']['x'] >25:
                if eventi_df.loc[last_opponent+1, 'location']['x'] < 38:
                  if eventi_df.loc[i, 'minute'] - eventi_df.loc[last_opponent+1, 'minute'] == 1:
                    if eventi_df.loc[i, 'second'] <= 14:
                      e['shotType'] = 'CounterAttackShot'
                      shot.append(e)
                  elif eventi_df.loc[i, 'second'] - eventi_df.loc[last_opponent+1, 'second'] <= 15 and(eventi_df.loc[i, 'minute'] - eventi_df.loc[last_opponent+1, 'minute'] == 0):
                    e['shotType'] = 'CounterAttackShot'
                    shot.append(e)
                elif eventi_df.loc[last_opponent+1, 'location']['x'] > 38 and eventi_df.loc[last_opponent+1, 'location']['x'] < 66:
                  if eventi_df.loc[i, 'minute'] - eventi_df.loc[last_opponent+1, 'minute'] == 1:
                    if eventi_df.loc[i, 'second'] <= 11:
                      e['shotType'] = 'CounterAttackShot'
                      shot.append(e)
                  elif eventi_df.loc[i, 'second'] - eventi_df.loc[last_opponent+1, 'second'] <= 12 and (eventi_df.loc[i, 'minute'] - eventi_df.loc[last_opponent+1, 'minute'] == 0):
                    e['shotType'] = 'CounterAttackShot'
                    shot.append(e)

            else:
              if i-last_opponent <= 4 and eventi_df.loc[last_opponent +1, 'primary'] == 'interception':
                if 100 - eventi_df.loc[last_opponent+1, 'location']['x'] <=25:
                  e['shotType'] = 'BallRecoveryShot'
                  shot.append(e)







  shots_df = pd.DataFrame(shot)
  for z, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal
---------------------------------------------------------------------------------------
def get_positional_attacks(team_wyid, season_wyid = ''):
  shot = []
  j = 0
  shots_df = pd.DataFrame(shot)
  goal = 0
  shots = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & (eventi_df.primary != 'interception') & ('loss' not in eventi_df.secondary)]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      j = 0
      if e['primary'] == 'shot' and e['team_id'] == team_wyid and 'shot_after_free_kick' not in e['secondary']:
        last_opponent = (eventi_df.loc[i::-1, 'team_id'] != team_wyid).idxmax()
        for x in range(i, last_opponent, -1):
          if (eventi_df.loc[x, 'primary'] != 'throw_in' and eventi_df.loc[x, 'primary'] != 'free_kick' and eventi_df.loc[x, 'primary'] != 'corner'):
              j +=1
              if j>7:
                e['shotType'] = 'positionalAttack'
                shot.append(e)
                break
          else:
            j = 0
            break


  shots_df = pd.DataFrame(shot)
  for x, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1

  return shots_df, shots, goal

---------------------------------------------------------------------------------------
def get_corner_kick_schema(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  shots = 0
  goal = 0
  z = 0
  first_corner = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & (eventi_df.primary != 'interception') & ('loss' not in eventi_df.secondary)]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'shot' and e ['team_id'] == team_wyid:
        first_corner = ((eventi_df.loc[i::-1, 'primary'].eq('corner')) & (eventi_df.loc[i::-1, 'team_id'].eq(team_wyid))).idxmax()
        if i-first_corner != 0:
          if 'second_assist' in eventi_df.loc[i-2, 'secondary'] and eventi_df.loc[i-2, 'primary'] == 'corner':
            if 'cross' not in eventi_df.loc[i-1, 'secondary']:
              e['shotType'] = 'IndirectCornerKickWithCrossAndBounce'
              shot.append(e)
            else:
              e['shotType'] = 'IndirectCornerKickWithPassAndCross'
              shot.append(e)
          elif 'shot_assist' in eventi_df.loc[i-1, 'secondary'] and eventi_df.loc[i-1, 'primary'] == 'corner':
            e['shotType'] = 'IndirectCornerKickWithCross'
            shot.append(e)
          elif eventi_df.loc[i-2, 'primary'] == 'corner' and (eventi_df.loc[i-1,'primary'] == 'pass' and 'head_pass' in eventi_df.loc[i-1, 'secondary']):
            e['shotType'] = 'IndirectCornerKickWithCrossAndHeadBank'
            shot.append(e)
          elif eventi_df.loc[i-2, 'primary'] == 'corner' and (eventi_df.loc[i-1,'primary'] == 'pass' and 'head_pass' not in eventi_df.loc[i-1, 'secondary']):
            e['shotType'] = 'IndirectCornerKickWithCrossAndBank'
            shot.append(e)
          elif eventi_df.loc[i-2, 'primary'] == 'corner' and get_distance(eventi_df.loc[i-2, 'location']['x'], eventi_df.loc[i-2, 'location']['y'], eventi_df.loc[i-2, 'pass']['endLocation']['x'], eventi_df.loc[i-2, 'pass']['endLocation']['y']) < 3:
            if eventi_df.loc[i-1, 'primary'] == 'pass' and 'cross' in eventi_df.loc[i-1, 'secondary']:
              e['shotType'] = 'IndirectCornerKickWithTouchAndCross'
              shot.append(e)
            elif eventi_df.loc[i-1, 'primary'] == 'touch':
              e['shotType'] = 'IndirectCornerKickWithTwoTouches'
              shot.append(e)
            elif eventi_df.loc[i-1, 'primary'] == 'pass':
              e['shotType'] = 'IndirectCornerKickWithTouchAndPass'
              shot.append(e)
          elif eventi_df.loc[i-1, 'primary'] == 'corner' and get_distance(eventi_df.loc[i-1, 'location']['x'], eventi_df.loc[i-1, 'location']['y'], eventi_df.loc[i-1, 'pass']['endLocation']['x'], eventi_df.loc[i-1, 'pass']['endLocation']['y']) < 3:
            e['shotType'] = 'IndirectCornerKickWithTouch'
            shot.append(e)
          elif i-first_corner <=4:
            for x in range(i, first_corner-1, -1):
              if eventi_df.loc[x, 'primary'] == 'touch':
                z += 1
            if z == 1:
              e['shotType'] = 'IndirectFreeKickWithCrossAndBounce'
              shot.append(e)
            elif z == 2:
              e['shotType'] = 'IndirectFreeKickWithCrossAndTwoBounces'
              shot.append(e)
            elif z == 3:
              e['shotType'] = 'IndirectFreeKickWithCrossAndThreeBounces'
              shot.append(e)
            elif z == 4:
              e['shotType'] = 'IndirectFreeKickWithCrossAndFourBounces'
              shot.append(e)

  shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if s['shot']['isGoal'] == True:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal
-------------------------------------------------------------------------------------

def get_direct_corner_kick(team_wyid, season_wyid = ''):
  shot = []
  shots = 0
  shots_df = pd.DataFrame(shot)
  goal = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'corner' and e['team_id'] == team_wyid and 'shot' in e['secondary']:
        e['shotType'] = 'DirectCornerKick'
        shot.append(e)

  shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if 'goal' in s['secondary']:
      goal += 1
    else:
      shots += 1
  return shots_df, shots, goal


def get_own_goal(team_wyid, season_wyid = ''):
  shot = []
  own = 0
  shots_df = pd.DataFrame(shot)
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'own_goal' and e ['team_id'] == team_wyid:
        e['shotType'] = 'OwnGoal'
        shot.append(e)


  shots_df = pd.DataFrame(shot)
  for j,s in shots_df.iterrows():
    own += 1
  return shots_df, own

---------------------------------------------------------------------------------------
def get_gks_punch(team_wyid, season_wyid = ''):
  shot = []
  shots_df = pd.DataFrame(shot)
  shots = 0
  goals = 0
  for m in get_matches(team_wyid, season_wyid):
    eventi = get_events_per_match(m['matchId'])
    eventi_df = pd.DataFrame(eventi)
    eventi_df_type = pd.json_normalize(eventi_df['type'])
    eventi_df_team = pd.json_normalize(eventi_df['team'])
    eventi_df_team.columns = ['team_id', 'name', 'formation']
    eventi_df_team.drop(['name', 'formation'], axis = 1, inplace = True)
    eventi_df.drop(['type', 'team'], axis = 1, inplace = True)
    eventi_df = pd.concat((eventi_df, eventi_df_type, eventi_df_team), axis = 1)
    eventi_df = eventi_df[(eventi_df.primary != 'duel') & (eventi_df.primary != 'touch')]
    eventi_df = eventi_df.reset_index()
    for i, e in eventi_df.iterrows():
      if e['primary'] == 'shot' and e['team_id'] == team_wyid:
        if eventi_df.loc[i-1, 'primary'] == 'shot_against' and ('save' in eventi_df.loc[i-1, 'secondary'] or 'reflexes_save' in eventi_df.loc[i-1, 'secondary']):
          e['shotType'] = 'shotAfterPunch'
          shot.append(e)
  shots_df = pd.DataFrame(shot)
  for j, s in shots_df.iterrows():
    if 'goal' in e['secondary']:
      goals += 1
    else:
      shots += 1

  return shots_df, shots, goals
