import tensorflow as tf
from tensorflow import keras
import numpy as np

model = keras.models.load_model('common/random_model.keras')

inputData = np.load("minimax/positions.npy")
policyOutcomes = np.load("minimax/moveprobs.npy")
valueOutcomes = np.load("minimax/outcomes.npy")

print(policyOutcomes.shape)

model.fit(inputData, [policyOutcomes, valueOutcomes], epochs=512, batch_size=16)
model.save('supervised_model.keras')