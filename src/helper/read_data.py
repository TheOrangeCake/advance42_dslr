import csv
import sys
import logging
import coloredlogs

coloredlogs.install()


def read_dataset(data_train: str) -> dict[str, list[str]]:
    try:
        with open(data_train, mode='r') as file:
            reader = csv.DictReader(file)
            fields = reader.fieldnames or []
            columns = {name: [] for name in fields}
            for row in reader:
                for name in fields:
                    data = (row[name] or '').strip()
                    columns[name].append(data)
        return columns
    except IOError as ioe:
        logging.critical(f"Error opening file: {ioe}")
        sys.exit(-1)


def is_numeric_column(values: list[str]) -> bool:
    has_value = False
    for v in values:
        if v == '':
            continue
        has_value = True
        try:
            float(v)
        except ValueError:
            return False
    return has_value


def only_numeric(data: dict[str, list[str]]) -> dict[str, list[float]]:
    result = {}
    for name, values in data.items():
        if name.lower() == 'index':
            continue
        if not is_numeric_column(values):
            continue
        result[name] = [float(v) for v in values if v != '']
    return result
