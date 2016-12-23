from project_grapes.classical import full_run
from project_grapes.ann import run_forged, run_keras
from project_grapes.combined import autoencoder, neural_switcharoo
from project_grapes.misc import pull_data


grapes = pull_data(frame=1)


print("Running all experiments on Grapes/Wines database!")
print("Classifying by wine production region!")
print("*"*50)
print("PHASE 1: classic algorithms")
full_run(grapes)
print("*"*50)
print("PHASE 2: neural network classification")
print("PHASE 2A: Keras")
run_keras()
print("PHASE 2B: Brainforge")
run_forged()
print("*"*50)
print("PHASE 3: combined models")
print("PHASE 3A: autoencoder")
autoencoder()
print("PHASE 3B: neural switcharoo")
neural_switcharoo()
