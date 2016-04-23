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
    self.cacheFiveFactorRegression = [None] * 26

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
    if self.cacheFiveFactorRegression[index] is None:
      self.cacheFiveFactorRegression[index] = self._regression('r%d - RF | Mkt-RF, SMB, HML, RMW, CMA', self.researched[['Mkt_RF', 'SMB', 'HML', 'RMW', 'CMA']], index)
    return self.cacheFiveFactorRegression[index]

  def fiveFactorRegression(self, index=None):
    return self._producecAll(self._fiveFactorRegression, index)

  def _testFiveParam(self, index):
    fit = self._fiveFactorRegression(index).fit()
    return (
      fit.f_test('const = 0'),
      fit.f_test('(RMW = 0), (CMA = 0)')
    )

  def testFiveParam(self, index=None):
    return self._producecAll(self._testFiveParam, index)

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
  print 'const = 0: %s' % r.fit().f_test('const = 0')
  print
  # 6
  print '\n'.join(
    'Test for r%d\'s five-factor-regression:\n\tconst = 0: %s\n\tRMW = 0, CMA = 0: %s\n' % (i + 1, tests[0], tests[1])
    for i, tests in enumerate(lab.testFiveParam())
  )
  # TODO: decide upon Problem6*.
  # 7
  r = lab.fiveFactorRegression(1) # Choose Sample1
  print r
  print util.log.title('its robust-standard-error version')
  print
  print r.fit().get_robustcov_results().summary()
  print
  # TODO: still more problems left...

if __name__ == '__main__':
  main()
