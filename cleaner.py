'''
Removes duplicates rows from generated datasets.
'''

import csv

ENCOUNTERS = ['Kokytos', 'Pandaemonium', 'Themis', 'Athena', 'PallasAthena']

for encounter in ENCOUNTERS:
  db = set()
  out = []

  print('Cleaning {}.'.format(encounter))
  with open('dataset_{}.csv'.format(encounter), 'r') as ds_csv:
    for line in csv.reader(ds_csv):
      row = tuple(line[1:])
      if not row in db:
        out.append(line)
      db.add(row)
  print('  > New size:', len(db))

  with open('dataset_{}_cleaned.csv'.format(encounter), 'w', newline='') as ds_csv:
    writer = csv.writer(ds_csv)
    for row in out:
      writer.writerow(row)
  print('  > Done!')