import numpy as np
import os.path
from sklearn.model_selection import train_test_split
import click

@click.command()
@click.argument('loadfrom', type=str, required=True)
@click.argument('iso', type=str, required=True)

def traintestsplit(loadfrom, iso):
    # Define the ratio for the splits
    train_ratio = 0.6
    validation_ratio = 0.2
    test_ratio = 0.2
    
    # load data
    LOADFROM = loadfrom
    ISOTOPE = iso
    coords = np.load(LOADFROM + ISOTOPE + "_coords.npy")
    feats = np.load(LOADFROM + ISOTOPE + "_feats.npy")
    labels = np.load(LOADFROM + ISOTOPE + "_labels.npy")

    # Split the data into training, validation, and test sets
    coords_train, coords_temp, feats_train, feats_temp, labels_train, labels_temp = train_test_split(coords, feats, labels, test_size=1 - train_ratio, random_state=42)
    
    # Split the temporary sets into validation and test sets
    coords_val, coords_test, feats_val, feats_test, labels_val, labels_test = train_test_split(coords_temp, feats_temp, labels_temp, test_size=test_ratio / (test_ratio + validation_ratio), random_state=42)
    
    np.save(LOADFROM + ISOTOPE + "_coords_train.npy", coords_train)
    np.save(LOADFROM + ISOTOPE + "_coords_val.npy", coords_val)
    np.save(LOADFROM + ISOTOPE + "_coords_test.npy", coords_test)
    np.save(LOADFROM + ISOTOPE + "_feats_train.npy", feats_train)
    np.save(LOADFROM + ISOTOPE + "_feats_val.npy", feats_val)
    np.save(LOADFROM + ISOTOPE + "_feats_test.npy", feats_test)
    np.save(LOADFROM + ISOTOPE + "_labels_train.npy", labels_train)
    np.save(LOADFROM + ISOTOPE + "_labels_val.npy", labels_val)
    np.save(LOADFROM + ISOTOPE + "_labels_test.npy", labels_test)
    
    print("Train Coords Shape: ", end="")
    print(coords_train.shape)
    print("Train Feats Shape: ", end="")
    print(feats_train.shape)
    print("Train Labels Shape: ", end="")
    print(labels_train.shape)

    print("Train-Test Split Successful")

if __name__ == '__main__':
    traintestsplit()
