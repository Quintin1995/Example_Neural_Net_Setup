from __future__ import print_function
import tensorflow.keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras import backend as K
from parameters import Parameters
from utils import *
import os
import numpy as np
import json
import yaml



with open("runs/run.yaml") as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    settings = yaml.load(file)

    print(settings)


#load all parameters into an object
p = Parameters(settings)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#fix channel
if K.image_data_format() == "channels_first":
    x_train = x_train.reshape(x_train.shape[0], 1, p.img_rows, p.img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, p.img_rows, p.img_cols)
    input_shape = (1, p.img_rows, p.img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], p.img_rows, p.img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], p.img_rows, p.img_cols, 1)
    input_shape = (p.img_rows, p.img_cols, 1)

#conversion, normalization, and reshaping
x_train = x_train.astype("float32")
x_test = x_test.astype("float32")
x_train /= 255
x_test /= 255
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices
y_train = tensorflow.keras.utils.to_categorical(y_train, p.num_classes)
y_test = tensorflow.keras.utils.to_categorical(y_test, p.num_classes)


#define a simple model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(p.num_classes, activation="softmax"))

model.compile(
    loss=tensorflow.keras.losses.categorical_crossentropy,
    optimizer=tensorflow.keras.optimizers.Adadelta(),
    metrics=["accuracy"],
)

#create a csv logger
csv_logger = CSVLogger(p.full_path_of_history)

# Training
actual_begin_time = datetime.now()
history = model.fit(
    x_train,
    y_train,
    callbacks=[csv_logger],
    batch_size=p.batch_size,
    epochs=p.epochs,
    verbose=1,
    validation_data=(x_test, y_test),
)
end_time = datetime.now()
print("\nTraining time: {}\n".format(end_time - actual_begin_time))

#eval model
score = model.evaluate(x_test, y_test, verbose=0)

#some prints
print("\nTest loss:".format(str(score[0])))
print("Test accuracy: {}\n".format(score[1]))

#saving the model weights
model.save_weights(p.full_path_of_weights)
print("\nsaved model weights to: {}\n".format(p.full_path_of_weights))

plot_history(history, p)