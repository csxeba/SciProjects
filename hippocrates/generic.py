from csxdata import roots


def load_data(path=None):
    import pickle as pkl
    if path is None:
        path = roots["raw"] + "Project_Hippocrates/X_y_headers.pkl"
    X, y = pkl.load(open(path, "rb"))
    return X, y
