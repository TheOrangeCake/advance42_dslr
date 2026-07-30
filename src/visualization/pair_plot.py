#TO DO SYLVIE

#INDEPENDANT DONC DOIT RELIRE DEPUIS DATASET


#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402
from helper.plot import save_fig  # noqa: E402

def pair_plot():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")
    data = read_dataset(sys.argv[1])
    for i in data:
        print(i, data[i])
#    print(data)
if __name__ == "__main__":
    pair_plot()