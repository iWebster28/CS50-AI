import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = [] # numpy.ndarrays
    labels = [] # integers (category #)

    # Get folders (labels)
    # Get images for each folder/label

    base_dir = os.curdir + os.path.join(os.sep, data_dir)

    for folder in os.listdir(base_dir):
        if (int(folder) < NUM_CATEGORIES): # Assert valid folder
            # For each image in a subdirectory: 
            sub_dir = base_dir + os.path.join(os.sep, folder)
            for image in os.listdir(sub_dir):
                path = os.path.join(sub_dir, image)
                img = cv2.imread(path) # , mode = 'RGB'
                resize = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), interpolation = cv2.INTER_LINEAR)
                images.append(resize) # Store image
                labels.append(folder) # Store label

    # Return list
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential(name='Traffic Sign Identification')

    # Specify input shape
    model.add(tf.keras.layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))) # RGB depth => 3

    # 1st 2D Convolutional Layer
    # 32 filters
    # 3x3 kernel size
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
    #Convolve 2nd Time
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
    # Max Pooling
    model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2))) 
    # Batch Normalization - keeps the mean activation ~0, and the standard deviation for the activation ~1
    model.add(tf.keras.layers.BatchNormalization())

    # 3rd & 4th Convolution
    model.add(tf.keras.layers.Conv2D(32, (2, 2), activation='relu'))
    model.add(tf.keras.layers.Conv2D(32, (2, 2), activation='relu'))
    # Max Pooling
    model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2)))
    # Batch Normalization
    model.add(tf.keras.layers.BatchNormalization())

    # Flatten
    model.add(tf.keras.layers.Flatten())

    # Hidden layer
    tf.keras.layers.Dense(128, activation='relu')

    # Dropout
    tf.keras.layers.Dropout(0.50)

    # Output layer
    # NUM_CATEGORIES outputs (43)
    # softmax activation to give probabilities/confidence in results - ideal version of sigmoid function for multi-classification
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax'))
   
    # Diagnostic
    model.summary()

    # Training the CNN
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model 


if __name__ == "__main__":
    main()
