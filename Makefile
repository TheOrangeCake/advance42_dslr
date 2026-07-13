DATA_TEST = src/datasets/dataset_test.csv
DATA_TRAIN = src/datasets/dataset_train.csv
DATA_DUMMY = src/datasets/dummy.csv
DATA_DUMMY_2 = src/datasets/dummy2.csv

PYTHON = venv/bin/python3
PIP = venv/bin/pip
FLAKE = venv/bin/flake8

all: describe histogram

describe:
	$(PYTHON) src/describe/describe.py $(DATA_TRAIN)

histogram:
	$(PYTHON) src/visualization/histogram.py $(DATA_TRAIN)

require:
	$(PIP) freeze > requirements.txt

install:
	$(PYTHON) -m venv venv
	$(PIP) install -r requirements.txt

flake:
	$(FLAKE) src

dummy:
	$(PYTHON) src/describe/describe.py $(DATA_DUMMY)

dummy2:
	$(PYTHON) src/describe/describe.py $(DATA_DUMMY_2)

.PHONY: all describe histogram require install flake dummy