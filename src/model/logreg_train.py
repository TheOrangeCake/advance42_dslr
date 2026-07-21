#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
import math
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402

coloredlogs.install()

# Steps:
#  1 - [OK] Define a learning rate / step so training can be faster
#  2 - [OK] Define number of epochs
#  3 - [OK] Go through the dataset to get the min and max
#  4 - [OK] Normalize the data, if data is empty, put 0.5
#  5 - [OK] Convert column based data to row based data
#  6 - [OK] Initialize a set of weights (1 per feature) per house
#  7 - [OK]Loop each epochs
#  8 - - [OK] Loop each house
#  9 - - - Loop each student
# 10 - - - - Store the correct result: Same house 1, other house 0
# 11 - - - - Predict student house (sigmoid and etc. TBD)
# 12 - - - - Calculate error: correct result - prediction
# 13 - - - - Loop each feature
# 14 - - - - - Update the weights (thetas) based on error
# 15 - Write weights, min and max to a file for classification later
# 16 - Draw training history graph to validate the training (θ converge)

HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
SKIP = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
#  1 - [OK] Define a learning rate / step so training can be faster
STEP = 0.1
#  2 - [OK] Define number of epochs
EPOCHS = 1000


def train() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./logreg_train [Dataset path]')
        return
    else:
        logging.info(f"Logreg_train Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])

    features = [name for name in data.keys() if name not in SKIP]

    #  3 - [OK] Go through the dataset to get the min and max
    min_max = cal_min_max(features, data)
    #  4 - [OK] Normalize the data, if data is empty, put 0.5
    normalized = normalize(features, data, min_max)
    # 5 - [OK] Convert column based data to row based data
    rows = convert_to_rows(features, data, normalized)

    #  6 - [OK] Initialize a set of weights (1 per feature) per house
    houses = {house: {name: 0.0 for name in features} for house in HOUSES}

    # #  7 - [OK]Loop each epochs
    # for _ in range(EPOCHS):
    #     # 8 - [OK] Loop each house
    #     for house in HOUSES:


# Cost function:
# J(θ) = −(1/m) Σᵢ₌₁..m [ y⁽ⁱ⁾·log(hθ(x⁽ⁱ⁾)) + (1 − y⁽ⁱ⁾)·log(1 − hθ(x⁽ⁱ⁾)) ]
# i is individual student, so x⁽ⁱ⁾ just mean values of current student
# Plug in hypothesis on the right most side
# y⁽ⁱ⁾·log(hypothesis(x⁽ⁱ⁾)) + (1 − y⁽ⁱ⁾)·log(1 − hypothesis(x⁽ⁱ⁾))
# y is binary truth (so 1 or 0, in this case, belong to this house or not)
# If y == 1 -> 1·log(hypothesis) + 0·log(1−hypothesis) -> log(hypothesis)
# If y == 0 -> 0·log(hypothesis) + 1·log(1−hypothesis) -> log(1−hypothesis)
# log() is used here because the closer the value passed to log is to 0,
# the more negative log() gets (log(0.5) = -0.69 but log(0.01) = -4.6),
# so being more wrong costs more than being slightly wrong
# Σᵢ₌₁..m is the sum of all student,
# this mean we do the above for all student then sum them up
# (1/m) the sum divide to total student for average
# Since log() is negative, - at the start mean to flip to positive,
# this mean the smaller J is the better, best case is J = 0
# A wall of explanation for 7 lines of code, yay math!
def cost(
        rows: list[tuple[str, dict[str, float]]],
        house: str,
        weights: dict[str, float]
        ) -> float:
    total = 0.0
    for label, values in rows:
        y = 1.0 if label == house else 0.0  # same house -> true
        p = hypothesis(weights, values)
        total += y * math.log(p) + (1 - y) * math.log(1 - p)
    return -total / len(rows)


# Formula: hθ(x) = g(θᵀx)
# θ is the list of weight, x is list of value,  θᵀx is their dot product
# so right side will be evaluated to θ1*x1 + θ2*x2 + θ3*x3 + ... + θn*xn
# Used to score student, result is sent to sigmoid() to convert to probability
def hypothesis(weights: dict[str, float], values: dict[str, float]) -> float:
    z = 0.0
    for feature in weights:
        z += weights[feature] * values[feature]
    return sigmoid(z)


# Formula: g(z) = 1 / (1 + e^(-z))
# Used to map any real-valued number into a value between 0 and 1
# https://www.w3schools.com/python/ref_math_exp.asp
def sigmoid(z: float) -> float:
    if z < 0:
        e = math.exp(z)
        return e / (1 + e)
    return 1 / (1 + math.exp(-z))


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
