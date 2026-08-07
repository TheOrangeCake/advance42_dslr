#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
import math
import csv
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset, is_numeric_column  # noqa: E402
from helper.plot import save_fig  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402

coloredlogs.install()

HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
SKIP = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
COLORS = {
    "Gryffindor": "red",
    "Ravenclaw":  "blue",
    "Hufflepuff": "yellow",
    "Slytherin":  "green",
}

def train2():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./logreg_train [Dataset path]')
        return
    else:
        logging.info(f"Logreg_train Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])
    print("ciao")


"""
    alors il faut regarder la probablité de chaque étudiant pour chaque maison
    et après on choisi 1 maison par étudiant

    weights = tableau avec toutes les features(branches) init à zero
    ça va se calculer automatiquement

"""

if __name__ == "__main__":
    train2()