#!/usr/bin/env python3

import csv

SOURCE = "accuracy_dataset_train.csv"
DESTINATION = "accuracy_dataset_test.csv"


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