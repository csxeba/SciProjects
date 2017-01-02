from csxdata import CData

from SciProjects.grapes.classical import full_run
from SciProjects.grapes.ann import run_forged, run_keras
from SciProjects.grapes.combined import autoencoder, neural_switcharoo
from SciProjects.grapes import path, indepsn

grapes = CData(path, indepsn, headers=1, lower=True, feature="borregio")

print("Running all experiments on Grapes/Wines database!")
print("Classifying by wine production region!")
print("*"*50)
print("PHASE 1: classic algorithms")
full_run(grapes)
print("*"*50)
print("PHASE 2: neural network classification")
print("PHASE 2A: Keras")
run_keras(grapes)
print("PHASE 2B: Brainforge")
run_forged(grapes)
print("*"*50)
print("PHASE 3: combined models")
print("PHASE 3A: autoencoder")
autoencoder(grapes)
print("PHASE 3B: neural switcharoo")
neural_switcharoo(grapes)
