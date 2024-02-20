import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

def form_team(team:dict) -> list:
  ans = [0]*(len(JOB_MAP)-1)
  for job, parse in team.items():
    ans[JOB_MAP[job.lower()]-1] = parse
  return ans

def pred_pulls(label, regressor, team):
  print('-'*100)
  print('"{}"'.format(label))
  print(team)
  print('~ [{:.0f}] pulls'.format((regressor.predict([form_team(team)]))[0]))

ENCOUNTER_MAP = {
  '9': 'Kokytos',
  '10': 'Pandaemonium',
  '11': 'Themis',
  '12a': 'Athena',
  '12b': 'PallasAthena'
}

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

for encounter in ['9', '10', '11', '12a', '12b']:
  dataset = pd.read_csv('dataset_{}_cleaned.csv'.format(ENCOUNTER_MAP[encounter]))
  X = dataset.iloc[:, 1:-1].values
  y = dataset.iloc[:, -1].values
  ########################################################################################
  ## No data preprocesssing required. Handled in cleaner.py.
  
  ########################################################################################
  ## Data set splitting. Split into training and testing sets.
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

  ########################################################################################
  ## No feature scaling required. Features are FFXIV jobs represented by [0-100].
  #print(X_train[0])

  ########################################################################################
  ## Multiple Linear Regression
  mlr_regressor = LinearRegression()
  mlr_regressor.fit(X_train, y_train)
  y_pred_mlr = mlr_regressor.predict(X_test)

  ## MSE accuracy measurement
  #print('MSE (MLR):', mean_squared_error(y_test, y_pred_mlr))
  #print(' Score (Train):', mlr_regressor.score(X_train, y_train))
  #print(' Score (Test):', mlr_regressor.score(X_test, y_test))

  ########################################################################################
  ## The fun part: predictions.
  print('\nEncounter:', ENCOUNTER_MAP[encounter])

  p = {'DRK': 19, 'GNB': 48, 'WHM': 74, 'SCH': 43, 'NIN': 42, 'DNC': 25, 'BLM': 82, 'RDM': 45}
  pred_pulls('TOPs', mlr_regressor, p)
  continue
  quit()

  p = {'WAR': 50, 'GNB': 50, 'WHM': 50, 'SCH': 50, 'MNK': 50, 'DNC': 50, 'SMN': 50, 'RDM': 50}
  pred_pulls('Average 50s', mlr_regressor, p)
  p = {'WAR': 50, 'GNB': 50, 'WHM': 50, 'SCH': 50, 'MNK': 50, 'SAM': 50, 'DNC': 50, 'BLM': 50}
  pred_pulls('Where is the battle raise?', mlr_regressor, p)

  p = {'WAR': 100, 'GNB': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'DNC': 100, 'SMN': 100, 'RDM': 100}
  pred_pulls('Bunch of try-hard 100s', mlr_regressor, p)
  p = {'WAR': 100, 'GNB': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'SAM': 100, 'DNC': 100, 'BLM': 100}
  pred_pulls('Who needs battle raise?', mlr_regressor, p)
  quit()

  p = {'WAR': 100, 'GNB': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'DNC': 100, 'SMN': 100, 'RDM': 100}
  pred_pulls('All-Stars 100s', mlr_regressor, p)
  p = {'WAR': 50, 'GNB': 50, 'WHM': 50, 'SCH': 50, 'MNK': 50, 'DNC': 50, 'SMN': 50, 'RDM': 50}
  pred_pulls('Average 50s', mlr_regressor, p)
  p = {'WAR': 1, 'GNB': 1, 'WHM': 1, 'SCH': 1, 'MNK': 1, 'DNC': 1, 'SMN': 1, 'RDM': 1}
  pred_pulls('Newbie 1s', mlr_regressor, p)
  p = {'WAR': 1, 'GNB': 1, 'WHM': 1, 'SCH': 1, 'MNK': 1, 'DNC': 1, 'SMN': 1, 'RDM': 100}
  pred_pulls("I can't carry you RDM.", mlr_regressor, p)
  p = {'WAR': 1, 'GNB': 1, 'WHM': 1, 'SCH': 1, 'MNK': 1, 'SAM': 1, 'DNC': 1, 'BLM': 1}
  pred_pulls('Where is the battle raise?', mlr_regressor, p)
  p = {'PLD': 100, 'GNB': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'DNC': 100, 'SMN': 100, 'RDM': 100}
  pred_pulls('Sub WAR->PLD', mlr_regressor, p)
  p = {'PLD': 100, 'WAR': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'DNC': 100, 'SMN': 100, 'RDM': 100}
  pred_pulls('Sub GNB->PLD', mlr_regressor, p)
  p = {'WAR': 100, 'GNB': 100, 'WHM': 100, 'SCH': 100, 'MNK': 100, 'DNC': 100, 'BLM': 100, 'RDM': 100}
  pred_pulls('Sub SMN->BLM', mlr_regressor, p)
quit()

# These following models are kinda... bad.

########################################################################################
## LDA dimensionality reduction
lda = LinearDiscriminantAnalysis(n_components=8)
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)

## Multiple Linear Regression (LDA)
mlr_lda_regressor = LinearRegression()
mlr_lda_regressor.fit(X_train_lda, y_train)
y_pred_mlr_lda = mlr_lda_regressor.predict(X_test_lda)

## MSE accuracy measurement(LDA)
print('MSE (MLR+LDA):', mean_squared_error(y_test, y_pred_mlr_lda))
print(' Score (Train):', mlr_lda_regressor.score(X_train_lda, y_train))
print(' Score (Test):', mlr_lda_regressor.score(X_test_lda, y_test))

#np.set_printoptions(precision=2)
#print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

########################################################################################
## Decision Tree Regression
tree_regressor = DecisionTreeRegressor(random_state=0)
tree_regressor.fit(X_train, y_train)
y_pred_tree = tree_regressor.predict(X_test)

## MSE accuracy measurement(DT)
print('MSE (DT):', mean_squared_error(y_test, y_pred_tree))
print(' Score (Train):', tree_regressor.score(X_train, y_train))
print(' Score (Test):', tree_regressor.score(X_test, y_test))

########################################################################################
## Random Forest Tree Regression
forest_regressor = RandomForestRegressor(random_state=0)
forest_regressor.fit(X_train, y_train)
y_pred_forest = forest_regressor.predict(X_test)

## MSE accuracy measurement(RF)
print('MSE (RF):', mean_squared_error(y_test, y_pred_forest))
print(' Score (Train):', forest_regressor.score(X_train, y_train))
print(' Score (Test):', forest_regressor.score(X_test, y_test))