import cv2
import pickle
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data and images folders
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "images"

# Create data folder if it does not exist
DATA_DIR.mkdir(exist_ok=True)

image_data = []
labels = []


# Read all images from the images folder
for image_name in IMG_DIR.iterdir():

    if image_name.is_file():

        image = cv2.imread(str(image_name))

        if image is not None:

            image = cv2.resize(image, (100, 100))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            image_data.append(image)
            labels.append(image_name.name.split("_")[0])


# Convert lists to NumPy arrays
image_data = np.array(image_data)
labels = np.array(labels)


print("Image data shape:", image_data.shape)
print("Labels shape:", labels.shape)


# Display one sample image
if len(image_data) > 50:

    plt.imshow(image_data[50], cmap="gray")
    plt.show()


# Save processed image data
with open(DATA_DIR / "images.p", "wb") as f:
    pickle.dump(image_data, f)


# Save labels
with open(DATA_DIR / "labels.p", "wb") as f:
    pickle.dump(labels, f)


print("Data consolidation completed successfully.")