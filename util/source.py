import pandas as pd
import os

dataDir = os.path.realpath(os.path.join(__file__, '../../data')) + '/'

def read(dataName, suffix='.csv', prefix=dataDir):
  return pd.read_csv(prefix + dataName + suffix)
