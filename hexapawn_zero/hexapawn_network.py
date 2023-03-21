from keras.models import Model
from keras.layers import *
import numpy as np
import tensorflow as tf
'''
This Python code defines a neural network model using the Keras library (which runs on top of TensorFlow) to handle the game of hexapawn. I'll explain each line of the code below:

from keras.models import Model: Import the Model class from the Keras library. This class will be used to define the neural network model.

from keras.layers import *: Import all layer classes from the Keras library. These classes will be used to define the various layers of the neural network.

import numpy as np: Import the NumPy library and give it the alias 'np'. NumPy is a widely used library for numerical operations in Python.

import tensorflow as tf: Import the TensorFlow library and give it the alias 'tf'. TensorFlow is a popular library for machine learning and deep learning.

inp = Input((21,)): Define the input layer of the neural network with 21 input units (corresponding to the size of the input).

6-10. These lines define the hidden layers of the neural network. There are five dense layers (also known as fully connected layers), each with 128 hidden units and using the ReLU (Rectified Linear Unit) activation function.

l1 = Dense(128, activation='relu')(inp)
l2 = Dense(128, activation='relu')(l1)
l3 = Dense(128, activation='relu')(l2)
l4 = Dense(128, activation='relu')(l3)
l5 = Dense(128, activation='relu')(l4)
policyOut = Dense(28, name='policyHead', activation='softmax')(l5): Define the policy output layer, which has 28 output units and uses the softmax activation function to produce a probability distribution over possible moves.

valueOut = Dense(1, name='valueHead', activation='tanh')(l5): Define the value output layer, which has a single output unit and uses the tanh activation function to estimate the value of the current board position.

bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False): Define the categorical crossentropy loss function for the policy head. This is used to measure the difference between the predicted move probabilities and the true move probabilities.

model = Model(inp, [policyOut, valueOut]): Create the neural network model by specifying the input layer, and the two output layers (policy and value heads).

15-18. Compile the model, specifying the optimizer (Stochastic Gradient Descent, or 'SGD') and the loss functions for the two output layers. The value head uses mean squared error as its loss function, and the policy head uses the previously defined categorical crossentropy loss function.

model.compile(optimizer='SGD', loss={'valueHead': 'mean_squared_error', 'policyHead': bce})
model.save('random_model.keras'): Save the neural network model to a file named 'random_model.keras'.
'''

# Define Network input
inp = Input((21,))

# Define Network layers
l1 = Dense(128, activation='relu')(inp)
l2 = Dense(128, activation='relu')(l1)
l3 = Dense(128, activation='relu')(l2)
l4 = Dense(128, activation='relu')(l3)
l5 = Dense(128, activation='relu')(l4)

# Define Network output
policyOut = Dense(28, name='policyHead', activation='softmax')(l5)
valueOut = Dense(1, name='valueHead', activation='tanh')(l5)

# Define Network model
bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
model = Model(inp, [policyOut, valueOut])
model.compile(optimizer='SGD',
              loss={'valueHead': 'mean_squared_error', 
                    'policyHead': bce})

model.save('random_model.keras')