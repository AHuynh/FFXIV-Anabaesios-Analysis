'''
Collects rows of static clears from the Anabaesios Savage FFXIV raid tier.
The output is, per fight, a row consisting of each of a guild ID, each of
FFXIV's jobs represented as a Med. Avg. Parse [0-100] (0 means job not in
composition), and the number of pulls this static took to clear the fight.
'''

from config import CLIENT_ID, CLIENT_SECRET
from fflogsapi import FFLogsClient 

import csv
import time

STARTING_ID = 117996  # Some very recent guild ID.
DIFF_SAVAGE = 101
TIME_INTERVAL = 10
time_tick = TIME_INTERVAL
successful_rows = 0

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
print('Client created.')

def check_remaining_points(client) -> float:
  '''
  Returns the number of API limit points remaining.
  Doesn't seem to actually do anything. It's probably reading the cache.
  '''
  limit = client.q('query{rateLimitData{limitPerHour}}')
  spent = client.q('query{rateLimitData{pointsSpentThisHour}}')
  return limit['rateLimitData']['limitPerHour'] - spent['rateLimitData']['pointsSpentThisHour']

def write_entry(row: list, encounter: str):
  '''
  Write a new row to an encounter's database.
  '''
  print('~'*80)
  print('Writing new entry for', encounter)
  print(row)
  with open('dataset_{}.csv'.format(encounter), 'a+', newline='') as dataset:
    writer = csv.writer(dataset)
    writer.writerow(row)
  print('~'*80)

def write_seen_guilds(client: FFLogsClient, new_seen_guilds: set):
  '''
  Update the list of guild IDs already seen.
  '''
  print('> Updating seen_guilds.csv...')
  with open('seen_guilds.csv', 'a+', newline='') as seen_guilds_file:
    seen_guilds_file.write('\n') 
    writer = csv.writer(seen_guilds_file)
    writer.writerow(new_seen_guilds)
  seen_guilds.update(new_seen_guilds)
  new_seen_guilds.clear()
  print('  Updated!')

def save_and_quit(client: FFLogsClient, guild_id: int=STARTING_ID, new_seen_guilds: set=None):
  '''
  Gracefully close out of the script.
  '''
  print('~'*80)
  guild_id += 1
  print('> Quitting on guild ID:', guild_id)
  with open('last_seen_id.txt', 'w') as last_seen_id:
    last_seen_id.write(str(guild_id))
  if new_seen_guilds:
    write_seen_guilds(client, new_seen_guilds)
  if client:
    print('> Updating cache...')
    client.save_cache(silent=False)
    print('  Updated!')
  quit()

JOB_MAP = {
  'GuildID': 0,
  'Paladin': 1,
  'Warrior': 2,
  'DarkKnight': 3,
  'Gunbreaker': 4,
  'WhiteMage': 5,
  'Scholar': 6,
  'Astrologian': 7,
  'Sage': 8,
  'Monk': 9,
  'Dragoon': 10,
  'Ninja': 11,
  'Samurai': 12,
  'Reaper': 13,
  'Bard': 14,
  'Machinist': 15,
  'Dancer': 16,
  'BlackMage': 17,
  'Summoner': 18,
  'RedMage': 19,
  'PullCount': 20
  }

JOB_ABBR = {
  'Paladin': 'PLD',
  'Warrior': 'WAR',
  'DarkKnight': 'DRK',
  'Gunbreaker': 'GNB',
  'WhiteMage': 'WHM',
  'Scholar': 'SCH',
  'Astrologian':'AST',
  'Sage': 'SGE',
  'Monk': 'MNK',
  'Dragoon': 'DRG',
  'Ninja': 'NIN',
  'Samurai': 'SAM',
  'Reaper': 'RPR',
  'Bard': 'BRD',
  'Machinist': 'MCH',
  'Dancer': 'DNC',
  'BlackMage': 'BLM',
  'Summoner': 'SMN',
  'RedMage': 'RDM',
  }

ENCOUNTER_MAP = {
  88: 'Kokytos',
  89: 'Pandaemonium',
  90: 'Themis',
  91: 'Athena',
  92: 'PallasAthena'
  }

# Exclude characters that cheated in stats.
BANLIST = set([
  ('Alfredo Saus', 'Jenova')
])

# Start off from the last seen guild.
with open('last_seen_id.txt', 'r') as last_seen_id:
  STARTING_ID = int(last_seen_id.read())
guild_id = STARTING_ID

# Start keeping track of seen guilds. If we see one we've already
# seen for some reason, we skip it.
seen_guilds = set()
new_seen_guilds = set()
with open('seen_guilds.csv', 'r') as seen_guilds_file:
  data = list(csv.reader(seen_guilds_file))
  for line in data:
    seen_guilds.update(line)

# Should be able to break with ^C.
try:
  # https://www.fflogs.com/v2-api-docs/ff/guilddata.doc.html
  '''
  I initially tried using guild_pagination_iterator, but
  it starts at page 1 (guild ID = 0), which is the oldest
  guild. It's reasonable to assume newer guilds will have
  a higher chance of clearing recent content, so I instead
  just start at a recent guild ID and count down.
  '''
  #gpi = client.guilds()  # guild_pagination_iterator
  #for guild_page in gpi:
  while True:
    #for guild in guild_page:
    for g_id in range(STARTING_ID, 1, -1):
      # Write to seen guilds every now and then
      time_tick -= 1
      if time_tick == 0:
        write_seen_guilds(client, new_seen_guilds)
        time_tick = TIME_INTERVAL

      print('='*80)
      #guild_id = guild.id
      guild_id = g_id
      if guild_id in seen_guilds:
        print('Already seen guild with ID:', guild_id)
        continue
      
      # Check point allotment. I don't think this works lol.
      if time_tick % 5 == 0:
        client.save_cache(silent=True)
        pts = check_remaining_points(client)
        print('Points remaining:', pts)
        if pts < 100:
          print('Points low! Quitting.')
          save_and_quit(client, guild_id, new_seen_guilds)
    
      print('Reading guild with ID:', guild_id)
      new_seen_guilds.add(guild_id)

      race_data = client.get_progress_race({
        'difficulty': DIFF_SAVAGE,
        'guildID': guild_id
        })

      print('='*80)
      print('Race data len:', len(race_data))
      for rd in race_data:
        print('-'*80) 
        for encounter in rd['encounters']:
          try:
            if encounter['id'] in ENCOUNTER_MAP:
              print('Encounter:', ENCOUNTER_MAP[encounter['id']])
            if not encounter['isKilled']:
              print("  > Encounter doesn't qualify.")
              continue
            # Encounter is valid and cleared. Now read jobs.
            encounter_row = [0]*len(JOB_MAP)
            encounter_row[JOB_MAP['PullCount']] = encounter['pullCount']
            print("  > Pull count:", encounter['pullCount'])
            print("  > Getting players...")
            # Try to read all 8 jobs. If we can, we can write the data.
            player_count = 0
            try:
              for role in encounter['composition']['roles']:
                if player_count == -1: break
                for player in role['players']:
                  if player_count == -1: break
                  if (player['name'], player['server']) in BANLIST:
                    print('    > Character is a cheater, stopping.')
                    player_count = -1
                    break
                  print('    Getting "{}" ({}) of {}, {}.'.format(player['name'], JOB_ABBR[player['type']], player['server'], rd['region']['shortName']))
                  character = client.get_character({
                    'name': player['name'],
                    'serverSlug': player['server'],
                    'serverRegion': rd['region']['shortName']
                    })
                  print('    > Character retrieved.')
                  parse = -1
                  try:
                    # Prefer the character's overall median performance.
                    zr = character.zone_rankings({
                      'byBracket': False,
                      'difficulty': DIFF_SAVAGE,
                      'specName': player['type']
                      })
                    print('    > Zone rankings retrieved.')
                    parse = zr.median_performance_avg
                  except Exception as ex_zone:
                    # Fallback to the character's specific encounter median performance.
                    er = character.encounter_rankings({
                      'byBracket': False,
                      'difficulty': DIFF_SAVAGE,
                      'encounterID': encounter['id'],
                      'specName': player['type']
                      })
                    print('    > Encounter rankings retrieved.')
                    parse = er.median_performance_avg
                  finally:
                    if parse == -1:
                      print('    > Unable to retrieve character rankings.')
                      player_count = -1
                      break
                    print('    > OK!', player['type'], parse)
                    encounter_row[JOB_MAP[player['type']]] = parse
                    player_count += 1
                    if player_count == 8:
                      encounter_row[JOB_MAP['GuildID']] = guild_id
                      write_entry(encounter_row, ENCOUNTER_MAP[encounter['id']])
                      successful_rows += 1
            except Exception as ex_role:
              print('    Player Exception:', ex_role)
              break
            print("  < Done with getting players.")
          except Exception as ex:
            print("Exception:", ex)
            continue
except KeyboardInterrupt:
  print('#'*80)
  print('#'*80)
  print(">>> Quitting! Wrote {} rows.".format(successful_rows))
  print('#'*80)
  print('#'*80)
  save_and_quit(client, guild_id, new_seen_guilds)