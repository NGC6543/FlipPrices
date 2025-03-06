import pickle


def make_pickle(obj, path: str):
    """
    Save obj in pickle
    obj: object that we want save
    path: path to this object
    """
    dbfile = open(path, "wb")
    pickle.dump(obj, dbfile)
    dbfile.close()


def load_pickle(path: str):
    dbfile = open(path, "rb")
    db = pickle.load(dbfile)
    dbfile.close()
    return db
