DATA_TEST = src/datasets/dataset_test.csv
DATA_TRAIN = src/datasets/dataset_train.csv
DATA_DUMMY = src/datasets/dummy.csv
DATA_DUMMY_2 = src/datasets/dummy2.csv
DATA_DUMMY_TEST = src/datasets/dummy_test.csv
DATA_ACCURACY_TRAIN = src/datasets/accuracy_dataset_train.csv
DATA_ACCURACY_TEST = src/datasets/accuracy_dataset_test.csv

PYTHON = venv/bin/python3
PIP = venv/bin/pip
FLAKE = venv/bin/flake8

all: describe histogram scatter train

describe:
	$(PYTHON) src/describe/describe.py $(DATA_TRAIN)

histogram:
	$(PYTHON) src/visualization/histogram.py $(DATA_TRAIN)

histogram2:
	$(PYTHON) src/visualization/histogram2.py $(DATA_TRAIN)

scatter:
	$(PYTHON) src/visualization/scatter.py $(DATA_TRAIN)

pair:
	$(PYTHON) src/visualization/pair_plot.py $(DATA_TRAIN)

train:
	$(PYTHON) src/model/logreg_train.py $(DATA_TRAIN) $(DATA_DUMMY_TEST) $(ARGS)

predict:
	$(PYTHON) src/model/predict.py $(DATA_DUMMY_2) $(DATA_DUMMY_TEST) $(ARGS)

accuracy:
	$(PYTHON) src/model/accuracy.py $(DATA_TRAIN) $(DATA_ACCURACY_TEST) $(ARGS)

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

# to erase
data:
	$(PYTHON) src/helper/newread.py $(DATA_DUMMY)

.PHONY: all describe histogram scatter train require install flake dummy