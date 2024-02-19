'''
Visualize job perf. VS pulls to clear.
'''

import csv
import matplotlib.pyplot as plt

JOB_MAP = {
  'pld': 1,
  'war': 2,
  'drk': 3,
  'gnb': 4,
  'whm': 5,
  'sch': 6,
  'ast': 7,
  'sge': 8,
  'mnk': 9,
  'drg': 10,
  'nin': 11,
  'sam': 12,
  'rpr': 13,
  'brd': 14,
  'mch': 15,
  'dnc': 16,
  'blm': 17,
  'smn': 18,
  'rdm': 19,
  'PullCount': 20
  }

ENCOUNTER_MAP = {
  '9': 'Kokytos',
  '10': 'Pandaemonium',
  '11': 'Themis',
  '12a': 'Athena',
  '12b': 'PallasAthena'
  }

'''
Sample input:
blm 9
gnb 12a
q
'''
while True:
  try:
    i = input('> Encounter# Job or quit: ')
    if i.lower() == 'quit' or i.lower() == 'q':
      quit()
      break
    encounter, job = i.split(' ')
    encounter = encounter.strip().lower()
    job = job.strip().lower()
  except ValueError:
    print('Invalid input.')
    continue
  if not encounter in ENCOUNTER_MAP:
    print('Encounter not found (9, 10, 11, 12a, 12b).')
    continue
  if not job in JOB_MAP:
    print('Job not found.')
    continue

  parses = []
  pulls = []
  with open('dataset_{}_cleaned.csv'.format(ENCOUNTER_MAP[str(encounter)]), 'r') as dataset:
    data = list(csv.reader(dataset))
    for line in data:
      try:
        job_parse = float(line[JOB_MAP[job]])
        pull_count = int(line[JOB_MAP['PullCount']])
      except ValueError:
        continue
      if job_parse == 0:
        continue
      parses.append(job_parse)
      pulls.append(pull_count)
    print('    {} played {} times ({}%) out of {} total pulls.'.format(job.upper(), len(parses), round(100*len(parses)/len(data), 2), len(data), ))
    print('    Close plot to continue.')
  plt.title('{} parse VS Pull Count'.format(job.upper()))
  plt.scatter(parses, pulls, s=1)
  plt.xlabel("Parse %")
  plt.ylabel("# pulls to kill")
  plt.show()
  plt.close()