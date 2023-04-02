from keras.models import Model
from keras.layers import *
import numpy as np
import tensorflow as tf
'''
Network inputs
first 64 inputs is the position of the white pawns
next 64 inputs is the position of the white knights
next 64 inputs is the position of the white bishops
next 64 inputs is the position of the white rooks
next 64 inputs is the position of the white queens
next 64 inputs is the position of the white king
next 64 inputs is the position of the black pawns
next 64 inputs is the position of the black knights
next 64 inputs is the position of the black bishops
next 64 inputs is the position of the black rooks
next 64 inputs is the position of the black queens
next 64 inputs is the position of the black king
A 64 by 64 matrix to represent if a position has been repeated
A 64 by 64 matrix to represent if a position has been repeated twice
An 8 by 8 matrix to represent white's kingside castliong rights
an 8 by 8 matrix to represent white's queenside castling rights
An 8 by 8 matrix to represent black's kingside castling rights
an 8 by 8 matrix to represent black's queenside castling rights
This is a total of 12 64 by 64 matrices, so 12 * 64 * 64 = 49152 inputs
'''

inp = Input(shape=(8,8,18))

def residual_block(x, num_filters):
    res = x

    x = tf.keras.layers.Conv2D(filters=num_filters, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)

    x = tf.keras.layers.Conv2D(filters=num_filters, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.Add()([res, x])
    x = tf.keras.layers.Activation('relu')(x)

    return x

x = tf.keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), padding='same')(inp)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation('relu')(x)

num_blocks = 5  # adjust this to the desired number of residual blocks
num_filters = 256
for _ in range(num_blocks):
    x = residual_block(x, num_filters)

# Define Network output
# Policy head
policy_head = tf.keras.layers.Conv2D(filters=2, kernel_size=(1, 1), strides=(1, 1), padding='same')(x)
policy_head = tf.keras.layers.BatchNormalization()(policy_head)
policy_head = tf.keras.layers.Activation('relu')(policy_head)
policy_head = tf.keras.layers.Flatten()(policy_head)
policy_head = tf.keras.layers.Dense(units=num_legal_moves, activation='softmax', name='policy_output')(policy_head)

# Value head
value_head = tf.keras.layers.Conv2D(filters=1, kernel_size=(1, 1), strides=(1, 1), padding='same')(x)
value_head = tf.keras.layers.BatchNormalization()(value_head)
value_head = tf.keras.layers.Activation('relu')(value_head)
value_head = tf.keras.layers.Flatten()(value_head)
value_head = tf.keras.layers.Dense(units=64, activation='relu')(value_head)
value_head = tf.keras.layers.Dense(units=1, activation='tanh', name='value_output')(value_head)

# Create the model
model = tf.keras.Model(inputs=inp, outputs=[policy_head, value_head])

# Define Network model
bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
model = Model(inp, [policy_head, value_head])
model.compile(optimizer='SGD',
              loss={'valueHead': 'mean_squared_error', 
                    'policyHead': bce})

model.save('random_model.keras')