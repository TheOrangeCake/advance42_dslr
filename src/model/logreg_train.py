#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402

coloredlogs.install()


HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
SKIP = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
STEP = 0.1
EPOCHS = 1000

def train() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./logreg_train [Dataset path]')
        return
    else:
        logging.info(f"Logreg_train Dataset source: {sys.argv[1]}")
    
    data = read_dataset(sys.argv[1])

    # Initialize set of weights and bias
    features = [name for name in data.keys() if name not in SKIP]
    houses = {}
    for house in HOUSES:
        weights = {name: 0.0 for name in features}
        houses[house] = {"weights": weights, "bias": 0.0}
    
    min_max = cal_min_max(features, data)
    normalized = normalize(features, data, min_max)
    rows = convert_to_rows(features, data, normalized)

    # for _ in range(EPOCHS):
    #     for house in HOUSES:



    # Steps:
    #  1 - [OK] Initialize a set of weights per house. Each set has weight for all features (dont use only_numeric() as it left out the empty fields)
    #  3 - [OK] Initialize a bias per house
    #  2 - [OK] Define a learning rate / step so training can be faster
    #  4 - [OK] Define number of epochs
    #  5 - [OK] Go through the dataset to get the min and max
    #  6 - [OK] Normalize the data, if data is empty, put 0.5
    #  7 - [OK] Convert column based data to row based data
    #  8 - [OK]Loop each epochs
    #  9 - - [OK] Loop each house
    # 10 - - - Loop each student
    # 11 - - - - Store the correct result: Same house 1, other house 0
    # 12 - - - - Predict student house (sigmoid and etc. TBD)
    # 13 - - - - Calculate error: correct result - prediction
    # 14 - - - - Loop each feature
    # 15 - - - - - Update the weights (thetas) based on error
    # 16 - - - - Update bias
    # 17 - Write set data (weights, bias) and feature data (min, max) to a file for classification later
    # 18 - Draw training history graph to validate the training (theta converge)


# Calculate min and max for normalize
def cal_min_max(
        features: list[str],
        data: dict[str, list[str]]
        ) -> dict[str, dict[str, float]]:
    min_max = {}
    for name in features:
        values = sorted(float(v) for v in data[name] if v != '')
        min_max[name] = {"min": cal_min(values), "max": cal_max(values)}
    return min_max


def normalize(
        features: list[str],
        data: dict[str, list[str]],
        min_max: dict[str, dict[str, float]]
        ) -> dict[str, list[float]]:
    normalized = {}
    for name in features:
        low = min_max[name]["min"]
        high = min_max[name]["max"]
        span = high - low
        column = []
        for v in data[name]:
            if v == '' or span == 0:
                column.append(0.5)
            else:
                column.append((float(v) - low) / span)
        normalized[name] = column
    return normalized


# Convert column based read dataset to row based
def convert_to_rows(
        features: list[str],
        data: dict[str, list[str]],
        normalized: dict[str, list[float]]
        ) -> list[tuple[str, dict[str, float]]]:
    rows = []
    houses = data.get("Hogwarts House")
    if not houses:
        logging.critical('Missing or empty "Hogwarts House" column')
        sys.exit(-1)
    for i in range(len(houses)):
        values = {}
        for feature in features:
            values[feature] = normalized[feature][i]
        rows.append((houses[i], values))
    return rows


if __name__ == "__main__":
    train()
