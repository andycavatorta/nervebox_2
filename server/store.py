import shelve

shelve_path = None

def set(name, category, obj): 
  fullpath = shelve_path + category
  db = shelve.open(fullpath, 'c', 2)
  name_utf8 = name.encode()
  db[name_utf8] = obj
  db.close()

def get(name, category):
  fullpath = shelve_path + category
  db = shelve.open(fullpath, 'c', 2)
  name_utf8 = name.encode()
  obj = db[name_utf8]
  db.close()
  return obj
  
def delete(name, category): 
  fullpath = shelve_path + category
  db = shelve.open(fullpath, 'c', 2)
  success = False
  name_utf8 = name.encode()
  #print repr(db.keys())
  #print repr(name_utf8)
  try:
    del db[name_utf8]
    success = True
  except KeyError:
    success = False
  finally:
    db.close()
    return success
  
def listShelf(category):
  fullpath = shelve_path + category
  db = shelve.open(fullpath, 'c', 2)
  l = db.keys()
  return l
  
def listShelves():
  pass

def init(path):
  global shelve_path
  shelve_path = path
