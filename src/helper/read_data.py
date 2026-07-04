import csv
from typing import Iterator, TypedDict
import sys
import logging
import coloredlogs

coloredlogs.install()


class Student(TypedDict):
    Index: int
    Hogwarts_House: str
    First_Name: str
    Last_Name: str
    Birthday: str
    Best_Hand: str
    Arithmancy: float
    Astronomy: float
    Herbology: float
    Defense_Against_the_Dark_Arts: float
    Divination: float
    Muggle_Studies: float
    Ancient_Runes: float
    History_of_Magic: float
    Transfiguration: float
    Potions: float
    Care_of_Magical_Creatures: float
    Charms: float
    Flying: float


def read_dataset(data_train: str) -> Iterator[Student]:
    try:
        with open(data_train, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row
    except IOError as ioe:
        logging.critical(f"Error opening file: {ioe}")
        sys.exit(-1)
