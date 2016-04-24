import statsmodels.api as sm
import numpy as np
import pandas as pd
import util.source
import util.log
import util.format

# QUESTION: should I implement this myself?
def fgls(endog, exog):
  f = sm.OLS(endog, exog).fit()
  return sm.WLS(
    endog, exog,
    1 / np.exp(sm.OLS(
      np.log(f.resid ** 2),
      exog
    ).fit().predict())
  )

class Lab01:
  def __init__(self):
    self.researched = util.source.read('F-F_Research_Data_5_Factors_2x3')
    self.portfolios = util.source.read('25_Portfolios_5x5')
    self.cacheFiveFactorRegression = [None] * 26
    self.simpleFactor = sm.add_constant(self.researched.Mkt_RF)
    self.threeFactor = sm.add_constant(self.researched[['Mkt_RF', 'SMB', 'HML']])
    self.fourFactor = sm.add_constant(self.researched[['Mkt_RF', 'SMB', 'RMW', 'CMA']])
    self.fiveFactor = sm.add_constant(self.researched[['Mkt_RF', 'SMB', 'HML', 'RMW', 'CMA']])

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
      parameter
    ), title % index)

  def _producecAll(self, fn, index):
    return map(fn, xrange(1, 26)) if index is None else fn(index)

  def _simpleRegression(self, index):
    return self._regression('r%d | Mkt-RF', self.simpleFactor, index)

  def simpleRegression(self, index=None):
    return self._producecAll(self._simpleRegression, index)

  def _threeFactorRegression(self, index):
    return self._regression('r%d - RF | Mkt-RF, SMB, HML', self.threeFactor, index)

  def threeFactorRegression(self, index=None):
    return self._producecAll(self._threeFactorRegression, index)

  def _fiveFactorRegression(self, index):
    if self.cacheFiveFactorRegression[index] is None:
      self.cacheFiveFactorRegression[index] = self._regression('r%d - RF | Mkt-RF, SMB, HML, RMW, CMA', self.fiveFactor, index)
    return self.cacheFiveFactorRegression[index]

  def fiveFactorRegression(self, index=None):
    return self._producecAll(self._fiveFactorRegression, index)

  def fiveFactorFGLSRegression(self, index):
    return util.format.Model(fgls(
      self.portfolios['r' + str(index)] - self.researched.RF,
      self.fiveFactor
    ), 'FGLS: r%d - RF | Mkt-RF, SMB, HML, RMW, CMA' % index)

  def _testFiveParam(self, index):
    fit = self._fiveFactorRegression(index).fit()
    return (
      fit.f_test('const = 0'),
      fit.f_test('(RMW = 0), (CMA = 0)')
    )

  def testFiveParam(self, index=None):
    return self._producecAll(self._testFiveParam, index)

  def hmlRegression(self):
    return util.format.Model(sm.OLS(self.researched.HML, self.fourFactor), 'HML | Mkt-RF, SMB, RMW, CMA')

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
  INDEX_FOR_PROBLEM7 = 1  # Choose Sample1
  r = lab.fiveFactorRegression(INDEX_FOR_PROBLEM7)
  print r
  print util.log.title('its robust-standard-error version')
  f = r.fit()
  print
  print f.get_robustcov_results().summary()
  print
  # 8
  # QUESTION: these results differ from stata's.
  # Detail:
  # - White's test does not present chi2's df for heteroskedasticity.
  # - For White's test, Cameron & Trivedi's decomposition of IM-test is missing, i.e.
  #   - Skewness and Kurtosis are missing. Should have chi2, df, p for each.
  # - BP test has got a different result. Stata says `chi2(1) = 17.91, Prob > chi2 = 0.0000`. We get 11.652284 and 0.039876.
  # - Have no idea what Jarque Bera's test does.
  print 'White\'s test: lm = %f, lmpval = %f, fval = %f, fpval = %f\n' % sm.stats.het_white(f.resid, lab.fiveFactor)
  print 'Jarque Bera\'s test: jb = %f, jb_uv = %f, skew = %f, kurtosis = %f\n' % sm.stats.jarque_bera(f.resid)
  print 'Breusch-Pagan\'s test: lm = %f, lmpval = %f, fval = %f, fpval = %f\n' % sm.stats.het_breushpagan(f.resid, lab.fiveFactor)
  print lab.fiveFactorFGLSRegression(INDEX_FOR_PROBLEM7)

if __name__ == '__main__':
  main()
