import log

def joinAllStr(array, delimeter='\n'):
  return delimeter.join(map(str, array))

class Model:

  def __init__(self, model, title='Model'):
    self.model = model
    self.title = title
    self._fit = None
    self._summary = None

  def __str__(self):
    return log.title(self.title) + '\n\n' + str(self.summary()) + '\n'

  def fit(self):
    if self._fit is None:
      self._fit = self.model.fit()
    return self._fit

  def summary(self):
    if self._summary is None:
      self._summary = self.fit().summary()
    return self._summary
