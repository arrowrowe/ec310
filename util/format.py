import log

def joinAllStr(array, delimeter='\n'):
  return delimeter.join(map(str, array))

def produceAll(iterator):
  def decorator(fn):
    def decorated(one, index=None):
      return [
        fn(one, index=i) for i in iterator
      ] if index is None else fn(one, index)
    return decorated
  return decorator

def cacheDecorator(fn):
  cache = {}
  def decorated(one, index):
    if index not in cache:
      cache[index] = fn(one, index)
    return cache[index]
  return decorated

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
