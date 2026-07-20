#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402

coloredlogs.install()


houses = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
skip = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]


def train() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./logreg_train [Dataset path]')
        return
    else:
        logging.info(f"Logreg_train Dataset source: {sys.argv[1]}")
    
    data = read_dataset(sys.argv[1])

    # Steps:
    #  1 - Initialize a set of weights per house. Each set has weight for all features (dont use only_numeric() as it left out the empty fields)
    #  3 - Initialize a bias per house
    #  2 - Define a learning rate / step so training can be faster
    #  4 - Define number of epochs
    #  5 - Go through the dataset to get the min and max
    #  6 - Normalize the data, if data is empty, put 0.5
    #  7 - Loop each epochs
    #  8 - - Loop each house
    #  9 - - - Loop each student
    # 10 - - - - Store the correct result: Same house 1, other house 0
    # 11 - - - - Predict student house (sigmoid and etc. TBD)
    # 12 - - - - Calculate error: correct result - prediction
    # 13 - - - - Loop each feature
    # 14 - - - - - Update the weights (thetas) based on error
    # 15 - - - - Update bias
    # 15 - Write set data (weights, bias) and feature data (min, max) to a file for classification later
    # 16 - Draw training history graph to validate the training (theta converge)


if __name__ == "__main__":
    train()
