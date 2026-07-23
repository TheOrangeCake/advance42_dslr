# advance42_dslr

## dev installation
- Start by install and run Virtual Environement:
```sh
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
```
- Update dependency list for venv:
```sh
	pip freeze > requirements.txt
```
- Lint:
```sh
	flake8 src
```
- Venv:
```sh
	source venv/bin/activate
```

## Resources
- [Logistic regression](https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/)

## General structure

dslr/
├── README.md                 Project setup instructions <b>
├── Makefile                  Short commands for running each part <b>
├── requirements.txt          External Python packages <b>
├── src/ <b>
│   ├── datasets/             Training, testing, and dummy CSV data <b>
│   ├── helper/               Code shared by multiple programs <b>
│   ├── describe/             Statistical analysis <b>
│   ├── visualization/        Histograms and scatter plots <b>
│   └── model/                Logistic-regression training <b>
└── subjects/ <b>
    ├── en.subject.pdf        Original school assignment <b>
    └── datasets/             Original copies of the datasets <b>