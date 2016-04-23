import log

def strModel(model, title='Model'):
  return log.title(title) + '\n\n' + str(model.fit().summary()) + '\n'
