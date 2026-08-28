#!/usr/bin/env python3

"""
import csv

SOURCE = "../datasets/accuracy_dataset_train.csv"
DESTINATION = "../datasets/accuracy_dataset_test.csv"

def create_accuracy_test_file() -> None:
    with open(SOURCE, "r", newline="") as src:
        reader = csv.DictReader(src)

        if reader.fieldnames is None:
            raise ValueError("Missing CSV header")

        with open(DESTINATION, "w", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)

            writer.writeheader()

            for row in reader:
                row["Hogwarts House"] = ""
                writer.writerow(row)


if __name__ == "__main__":
    create_accuracy_test_file()

"""

import csv


def create_accuracy_test_file(
    source_train: str,
    destination_test: str
) -> None:
    with open(source_train, "r", newline="") as src:
        reader = csv.DictReader(src)

        if reader.fieldnames is None:
            raise ValueError("Missing CSV header")

        with open(destination_test, "w", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                row["Hogwarts House"] = ""
                writer.writerow(row)