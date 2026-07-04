#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
import coloredlogs
from min_max_perc import cal_min, cal_max, cal_per
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset, only_numeric  # noqa: E402

coloredlogs.install()


class Feature():
    def __init__(self, name):
        self.name = name
    name: str
    count: float
    mean: float
    std: float
    min: float
    quarter: float
    half: float
    three_quarter: float
    max: float


def describe() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./describe [Dataset path]')
        return
    else:
        logging.info(f"Dataset source: {sys.argv[1]}")

    data = only_numeric(read_dataset(sys.argv[1]))
    features: list[Feature] = []
    for name, values in data.items():
        values.sort()
        feature = Feature(name)
        feature.min = cal_min(values)
        feature.quarter = cal_per(values, 25)
        feature.half = cal_per(values, 50)
        feature.three_quarter = cal_per(values, 75)
        feature.max = cal_max(values)
        # Insert more calculation here
        features.append(feature)

    # print formated
    for feature in features:
        print(feature.name, feature.min, feature.max,
              feature.quarter, feature.half, feature.three_quarter)
    return


if __name__ == "__main__":
    describe()
