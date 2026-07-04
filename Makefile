DESCRIBE = describe
VISUALIZATION = visualization
MODEL =

DATA_TEST = src/datasets/datasets_test.csv
DATA_TRAIN = src/datasets/dataset_train.csv

all: describe flake

describe:
	python3 src/describe/describe.py $(DATA_TRAIN)

venv:
	python3 -m venv venv
	source venv/bin/activate

install:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

require:
	pip freeze > requirements.txt

flake:
	flake8 src