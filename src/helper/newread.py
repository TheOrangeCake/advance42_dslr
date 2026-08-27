import csv
import sys
import logging
import coloredlogs
from read_data import import_data, course_data, get_courses_list, get_houses_list, nb_students

def main():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./describe [Dataset path]')
        return
    else:
        logging.info(f"Dataset source: {sys.argv[1]}")

    data = import_data(sys.argv[1])
    for i in data:
      print(i," :: ", data[i])

    print(course_data(data, "Astronomy"))

    list = get_courses_list(data)
    print(list)

    print(get_houses_list(data))
    print(nb_students(data))
main()