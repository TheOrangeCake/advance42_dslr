#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402

coloredlogs.install()


def describe() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./describe [Dataset path]')
        return
    else:
        logging.info(f"Dataset source: {sys.argv[1]}")
    for row in read_dataset(sys.argv[1]):
        # do stuffs here for each row
        print(row)
    return


if __name__ == "__main__":
    describe()
