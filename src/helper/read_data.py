import csv
import sys
import logging
import coloredlogs

coloredlogs.install()

fields = [
    "Index", "Hogwarts House", "First Name",
    "Last Name", "Birthday", "Best Hand",
    "Arithmancy", "Astronomy", "Herbology",
    "Defense Against the Dark Arts", "Divination",
    "Muggle Studies", "Ancient Runes", "History of Magic",
    "Transfiguration", "Potions", "Care of Magical Creatures",
    "Charms", "Flying"
]


def read_dataset(data_train: str) -> dict[str, list[str]]:
    try:
        with open(data_train, mode='r') as file:
            reader = csv.DictReader(file)
            columns = {name: [] for name in fields}
            for row in reader:
                for name in fields:
                    data = row[name].strip()
                    columns[name].append(data)
        return columns
    except IOError as ioe:
        logging.critical(f"Error opening file: {ioe}")
        sys.exit(-1)


numeric_fields = [
    "Arithmancy", "Astronomy", "Herbology",
    "Defense Against the Dark Arts", "Divination", "Muggle Studies",
    "Ancient Runes", "History of Magic", "Transfiguration",
    "Potions", "Care of Magical Creatures", "Charms", "Flying",
]


def only_numeric(data: dict[str, list[str]]) -> dict[str, list[float]]:
    result = {}
    for name in numeric_fields:
        result[name] = []
        for v in data[name]:
            if v == '':
                continue
            result[name].append(float(v))
    return result
