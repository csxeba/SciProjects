import pickle

from SciProjects.hippocrates.generic import load_data, roots
from keras.models import Sequential
from keras.layers import MaxPooling3D


X, y = load_data()


model = Sequential()
model.add(MaxPooling3D(input_shape=X.shape[1:]))
model.compile("sgd", "mse")

X_ds = model.predict(X)

print("Oldshape:", X.shape)
print("Newshape:", X_ds.shape)

with open(roots["raw"] + "Project_Hippocrates/X_ds_y_labels.pkl", "wb") as outfl:
    pickle.dump((X_ds, y), outfl)
    outfl.close()
