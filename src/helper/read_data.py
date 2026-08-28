import csv
import sys
import logging
import coloredlogs
import numpy as np

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



'''
STRATEGY:
read datas and keep all in str. 
then extract numpy with what you need.
but always keep all names somewhere

select datas and return numpy: 
by branch
by house
by student. 

check what is needed in all the project. 
'''

def import_data(data_train: str)-> dict[str, list[str]]:
    data = read_dataset3(data_train)
    remove_useless_data(data)
    empty_values(data)
    return data

def read_dataset3(data_train: str) -> dict[str, list[str]]:
    try:
        with open(data_train, mode='r') as file:
            reader = csv.DictReader(file)
            fields = reader.fieldnames or []
            columns = {name: [] for name in fields}
            for row in reader:
                for name in fields:
                    data = (row[name] or '').strip()
                    columns[name].append(data)
    ##déplacer ces deux. 
       # data = remove_useless_data(columns)
        #data = empty_values(data)
        return columns
    except IOError as ioe:
        logging.critical(f"Error opening file: {ioe}")
        sys.exit(-1)

def remove_useless_data(data: dict[str, list[str]]) -> None:
    data.pop("Index")
    data.pop("First Name")
    data.pop("Last Name")
    data.pop("Birthday")
    data.pop("Best Hand")
    return data
    
#then it is easier to convert empty values
def empty_values(data: dict[str, list[str]]) -> None:
  for column in data:
      for i in range(len(data[column])):
          if data[column][i] == "":
              data[column][i] = "nan"

## get courses list
def get_courses_list(data: dict[str, list[str]]) -> list[str]:
    courses_list = []
    for i in data:
        if i == "Hogwarts House":
            continue
        courses_list.append(i)
    return courses_list

## get houses list
def get_houses_list(data: dict[str, list[str]]) -> list[str]:
    if ("Hogwarts House") not in data:
        raise KeyError("No Hogwarts House in data set")
    houses_list = []
    for i in range(len(data["Hogwarts House"])):
        if data["Hogwarts House"][i] not in houses_list:
            houses_list.append(data["Hogwarts House"][i])
    return houses_list

## !!! mettre erreur
def nb_students(data: dict[str, list[str]]) -> int:
    return len(data["Hogwarts House"])

# get data by branch in numpy
#for part 1 and 2
def course_data(data: dict[str, list[str]], branch: str)-> np.ndarray:
  if branch not in data:
    raise KeyError("This course is not in data set")
  return np.array(data[branch], dtype=float)

def get_students_grades(data: dict[str, list[str]]):
    course_list = get_courses_list(data)
    for i in range(len(data[1])):
        for course in course_list:
            data[course][i]

"""

# proposal Sylvie
# dictionnary with lists str or float
def read_dataset2(data_train: str):
    try:
        with open(data_train, mode='r') as file:
            header = file.readline().strip().split(',')
            data = {col: [] for col in header}
            
            for line in file:
                values = line.strip().split(',')
                for col, val in zip(header, values):
                    # Si la valeur est vide, on garde None (ou NaN)
                    if val == '':
                        data[col].append(None)
                    else:
                        try:
                            data[col].append(float(val))
                        except ValueError:
                            data[col].append(val)
    
    except IOError as ioe:
        logging.critical(f"Error opening file: {ioe}")
        sys.exit(-1)
    
    return data
"""