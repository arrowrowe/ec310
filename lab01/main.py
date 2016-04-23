import statsmodels.api as sm
import numpy as np
import pandas as pd
import util.source
import util.log
import util.format

class Lab01:
  def __init__(self):
    self.researched = util.source.read('F-F_Research_Data_5_Factors_2x3')
    self.portfolios = util.source.read('25_Portfolios_5x5')

  def describe(self):
    return ('%s\n\n%s\n\n%s\n\n%s\n' % (
      util.log.title('Summary'),
      self.researched.ix[:, 1:7].describe(),
      self.portfolios.ix[:, 1:13].describe(),
      self.portfolios.ix[:, 13:26].describe()
    )).replace('\\\n', '\n')

  def _regression(self, title, parameter, index):
    return util.format.Model(sm.OLS(
      self.portfolios['r' + str(index)] - self.researched.RF,
      sm.add_constant(parameter)
    ), title % index)

  def _producecAll(self, fn, index):
    return map(fn, xrange(1, 26)) if index is None else fn(index)

  def _simpleRegression(self, index):
    return self._regression('r%d | Mkt-RF', self.researched.Mkt_RF, index)

  def simpleRegression(self, index=None):
    return self._producecAll(self._simpleRegression, index)

  def _threeFactorRegression(self, index):
    return self._regression('r%d - RF | Mkt-RF, SMB, HML', self.researched[['Mkt_RF', 'SMB', 'HML']], index)

  def threeFactorRegression(self, index=None):
    return self._producecAll(self._threeFactorRegression, index)

  def _fiveFactorRegression(self, index):
    return self._regression('r%d - RF | Mkt-RF, SMB, HML, RMW, CMA', self.researched[['Mkt_RF', 'SMB', 'HML', 'RMW', 'CMA']], index)

  def fiveFactorRegression(self, index=None):
    return self._producecAll(self._fiveFactorRegression, index)

  def hmlRegression(self):
    return util.format.Model(sm.OLS(
      self.researched.HML,
      sm.add_constant(self.researched[['Mkt_RF', 'SMB', 'RMW', 'CMA']])
    ), 'HML | Mkt-RF, SMB, RMW, CMA')

def main():
  lab = Lab01()
  # 1
  print lab.describe()
  # 2
  print util.format.joinAllStr(lab.simpleRegression())
  # 3
  print util.format.joinAllStr(lab.threeFactorRegression())
  # 4
  print util.format.joinAllStr(lab.fiveFactorRegression())
  # 5
  r = lab.hmlRegression()
  print r
  print r.fit().f_test('const = 0')
  # TODO: still more problems left...

if __name__ == '__main__':
  main()
