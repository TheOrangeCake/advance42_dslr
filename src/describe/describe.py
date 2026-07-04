#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
import coloredlogs
from min_max_perc import cal_min, cal_max, cal_per
from bonus_nan_range import cal_nan_count, cal_range
from display import display
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset, only_numeric  # noqa: E402
from helper.models import Feature  # noqa: E402

coloredlogs.install()


def describe() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./describe [Dataset path]')
        return
    else:
        logging.info(f"Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])
    filtered_data = only_numeric(data)
    features: list[Feature] = []
    for name, values in filtered_data.items():
        values.sort()
        feature = Feature(name)
        feature.min = cal_min(values)
        feature.quarter = cal_per(values, 25)
        feature.half = cal_per(values, 50)
        feature.three_quarter = cal_per(values, 75)
        feature.max = cal_max(values)
        feature.range = cal_range(values)
        feature.nan = cal_nan_count(data[name])
        # Insert more calculation here
        features.append(feature)

    display(features)
    return


if __name__ == "__main__":
    describe()
