import pickle
from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.optimizers import Adam


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"

# Load image data
with open(DATA_DIR / "images.p", "rb") as f:
    images = pickle.load(f)

# Load labels
with open(DATA_DIR / "labels.p", "rb") as f:
    labels = pickle.load(f)


print("Images shape:", images.shape)
print("Labels shape:", labels.shape)

print("Persons:", set(labels))


# Encode person names into numbers
le = LabelEncoder()
labels = le.fit_transform(labels)

print("Encoded labels:", set(labels))


# Number of persons
p = len(set(labels))

print("Total number of Persons:", p)


# Display one sample image
if len(images) > 90:
    plt.imshow(images[90], cmap="gray")
    plt.show()


# Image preprocessing
def preprocessing(img):
    img = cv2.equalizeHist(img)
    img = img.reshape(100, 100, 1)
    img = img / 255
    return img


images = np.array(list(map(preprocessing, images)))

print("Shape of Input:", images.shape)


# Convert labels to categorical format
labels = to_categorical(labels)


# Create CNN model
def Lenet_Model():

    model = Sequential()

    # Convolutional and ReLU Layer
    model.add(
        Conv2D(
            30,
            (5, 5),
            input_shape=(100, 100, 1),
            activation="relu"
        )
    )

    # MaxPooling Layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Convolutional and ReLU Layer
    model.add(
        Conv2D(
            15,
            (3, 3),
            activation="relu"
        )
    )

    # MaxPooling Layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Flatten Layer
    model.add(Flatten())

    # Hidden Layer
    model.add(Dense(50, activation="relu"))

    # Output Layer
    model.add(Dense(p, activation="softmax"))

    model.compile(
        Adam(learning_rate=0.01),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# Create and display model
model = Lenet_Model()

model.summary()


# Train the model
h = model.fit(
    images,
    labels,
    validation_split=0.1,
    epochs=10
)


# Save trained model
MODEL_PATH = BASE_DIR / "models" / "final_model.h5"

model.save(MODEL_PATH)

print("Model saved successfully at:", MODEL_PATH)