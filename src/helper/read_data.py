import csv
import sys
import logging
import coloredlogs

coloredlogs.install()

#read the csv file return the columns
#dict key feature like artimetic  herbology.... list les values
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


#enleve colone non numeric check
def is_numeric_column(values: list[str]) -> bool:
    has_value = False
    for v in values:
        if v == '':
            continue
        has_value = True
        try:
            float(v)
        except ValueError:
            # logging.warning(f"NaN detected: {v}, skipped column")
            return False
    return has_value

#enleve colone non numeric 
def only_numeric(data: dict[str, list[str]]) -> dict[str, list[float]]:
    result = {}
    for name, values in data.items():
        if name.lower() == 'index':
            continue
        if not is_numeric_column(values):
            continue
        result[name] = [float(v) for v in values if v != '']
    return result
