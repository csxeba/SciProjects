from csxdata import roots


def load_data(path=None):
    import pickle
    if path is None:
        path = roots["raw"] + "Project_Hippocrates/X_y_headers.pkl"
    X, y = pickle.load(open(path, "rb"))
    return X, y
