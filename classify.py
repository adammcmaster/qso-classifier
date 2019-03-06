import tensorflow as tf
from tensorflow import keras

import numpy as np

import csv

from random import shuffle


class ObjectClass:
    STAR = 0
    QSO = 1


INPUTS = (
    ('data/Stars.csv', ObjectClass.STAR),
    ('data/QSOs.csv', ObjectClass.QSO),
)

data = []

for filename, obj_class in INPUTS:
    with open(filename) as input_f:
        r = csv.DictReader(input_f)
        for row in r:
            data.append((
                float(row['u']) - float(row['g']),
                float(row['g']) - float(row['r']),
                obj_class,
            ))

shuffle(data)

train_data = data[100:]
train_labels = np.array([d[2] for d in train_data])
train_data = np.array([d[:2] for d in train_data])

test_data = data[:100]
test_labels = np.array([d[2] for d in test_data])
test_data = np.array([d[:2] for d in test_data])


model = keras.Sequential([
    keras.layers.Dense(2, activation=tf.nn.relu),
    keras.layers.Dense(8, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

model.fit(train_data, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_data, test_labels)

print('Test accuracy:', test_acc)
