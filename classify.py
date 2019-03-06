import tensorflow as tf
from tensorflow import keras

import numpy as np

import csv

from random import shuffle


object_classes = {
    'STAR': 0,
    'QSO': 1,
}

COLOUR_FIELDS = ('u', 'g', 'i', 'r', 'z')

data = []

with open('data/SDSS.csv') as input_f:
    r = csv.DictReader(input_f)
    for row in r:
        values = [object_classes[row['class']]]
        processed_fields = []
        for field in COLOUR_FIELDS:
            processed_fields.append(field)
            for field2 in COLOUR_FIELDS:
                if field2 in processed_fields:
                    continue
                values.append(float(row[field]) - float(row[field2]))
        data.append(values)

shuffle(data)

train_data = data[1000:]
train_labels = np.array([d[0] for d in train_data])
train_data = np.array([d[1:] for d in train_data])

test_data = data[:1000]
test_labels = np.array([d[0] for d in test_data])
test_data = np.array([d[1:] for d in test_data])


model = keras.Sequential([
    keras.layers.Dense(11, activation=tf.nn.relu),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

model.fit(train_data, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_data, test_labels)

print('Test accuracy:', test_acc)
