# advance42_dslr

## dev installation
- Start by install and run Virtual Environement:
```sh
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt //inside (venv)
```
- To update dependency list for vevn:
```sh
	pip freeze > requirements.txt
```
- To lint:
```sh
	flake8 src
```