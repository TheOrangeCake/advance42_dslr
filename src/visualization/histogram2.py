#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402
from helper.plot import save_fig  # noqa: E402
from pprint import pprint
#from describe.count_mean_std import cal_count 
coloredlogs.install()

from helper.read_data import read_dataset2  # noqa: E402
import describe.count_mean_std as cal


HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
SKIP = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
COLORS = {
    "Gryffindor": "red",
    "Ravenclaw":  "blue",
    "Hufflepuff": "yellow",
    "Slytherin":  "green",
}

COURSES = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]

COURSE_COLORS = {
    "Arithmancy": "tab:blue",
    "Astronomy": "tab:orange",
    "Herbology": "tab:green",
    "Defense Against the Dark Arts": "tab:red",
    "Divination": "tab:purple",
    "Muggle Studies": "tab:brown",
    "Ancient Runes": "tab:pink",
    "History of Magic": "tab:gray",
    "Transfiguration": "tab:olive",
    "Potions": "tab:cyan",
    "Care of Magical Creatures": "gold",
    "Charms": "navy",
    "Flying": "darkmagenta",
}

def get_data_house_course(data, house_name, branch):
    values = []

    for i in range(len(data['Hogwarts House'])):
        if data['Hogwarts House'][i] == house_name:
            val = data[branch][i]
            if val is not None and val != ''and val == val:
                values.append(val)
    return values

def homogeneity_index(data, course):
    course_scores = {course: [] for course in COURSES}

    mean_houses = []
    std_houses  = []
    dif_max_min = cal.diff_max_min(data[course])
      
    for house in HOUSES:
        house_course_data = get_data_house_course(data, house, course)
        count = cal.cal_count(house_course_data)
        mean = cal.cal_mean(house_course_data)
        std = cal.cal_std(house_course_data, count, mean)
        mean_houses.append(mean)
        std_houses.append(std)

    mean_spread = cal.diff_max_min(mean_houses)
    std_spread = cal.diff_max_min(std_houses)

    #mise à l'échelle
    mean_spread_norm = mean_spread / dif_max_min
    std_spread_norm = std_spread / dif_max_min

    index = mean_spread_norm + std_spread_norm
    return index


def histogram2() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    data = read_dataset2(sys.argv[1])
    house_col = data.get("Hogwarts House")
    if not house_col:
        logging.critical('Missing or empty "Hogwarts House" column')
        return
    
    plot = 1
    course_scores = {course: [] for course in COURSES}
    for course in COURSES:
#        count_of_branch = cal.cal_mean(data[course])
#        mean_of_branch = cal.cal_mean(data[course])
        #mise à l'échelle avec min max ???
        dif_max_min = cal.diff_max_min(data[course])
        
        #house_scores = {house: [] for house in HOUSES}
        
        for house in HOUSES:
            house_course_data = get_data_house_course(data, house, course)
            count = cal.cal_count(house_course_data)
            mean = cal.cal_mean(house_course_data)
            std = cal.cal_std(house_course_data, count, mean)
            std = std / dif_max_min
            print(house, ": ", std)
            #mise à l échelle ???
            course_scores[course].append(std)

    graph.subplot(1, 2, plot)
    # ici sortir le 
    for course in COURSES:
        print(course, ": ", course_scores[course])
        graph.hist(
            course_scores[course],
            label=course,
            color=COURSE_COLORS[course],
            alpha=0.5,
            edgecolor='black',
        )
        #graph.title(course)
    graph.title("Histogram2")
    handles, labels = graph.gca().get_legend_handles_labels()
    graph.figlegend(handles, labels, loc='lower right')
    save_fig("histogram", "histogram.png")
    graph.show()

""" 
def histogram2() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    data = read_dataset2(sys.argv[1])
    house_col = data.get("Hogwarts House")
    if not house_col:
        logging.critical('Missing or empty "Hogwarts House" column')
        return
    plot = 1

#    print(data)

#    print(data['First Name'])
    #print(type(data['Astronomy']))
#    for n in data['Astronomy']:
#        print(n)
#       print(type(n))

        #search in datas
#    count_1 = cal.cal_count((data['Astronomy']))
#    print("count ", count_1)
#    mean = cal.cal_mean(data['Astronomy'])
#    print("mean: ", mean)
#    print("std ", cal.cal_std(data['Astronomy'], count_1, mean))
#    get_data_house_course(data, "Hufflepuff", "Arithmancy")
    #print("get data house", get_data_house_course(data, "Hufflepuff", "Arithmancy"))


    for course in data.keys():
        if course in SKIP:
            continue
#        count_of_branch = cal.cal_mean(data[course])
#        mean_of_branch = cal.cal_mean(data[course])
        #mise à l'échelle avec min max ???
        #dif_max_min = cal.diff_max_min(data[course])
        
        house_scores = {house: [] for house in HOUSES}
        for house in HOUSES:
            house_course_data = get_data_house_course(data, house, course)
            count = cal.cal_count(house_course_data)
            mean = cal.cal_mean(house_course_data)
            std = cal.cal_std(house_course_data, count, mean)
            #mise à l échelle ???
            house_scores[house] = std

        graph.subplot(4, 4, plot)
        plot += 1
        for house in HOUSES:
            graph.hist(
                house_scores[house],
                label=house,
                color=COLORS[house],
                alpha=0.5,
                edgecolor='black',
            )
        graph.title(course)
    handles, labels = graph.gca().get_legend_handles_labels()
    graph.figlegend(handles, labels, loc='lower right')
    save_fig("histogram", "histogram.png")
    graph.show()
    # Conclusion:
    # Q: Which Hogwarts course has a homogeneous score
    #    distribution between all four houses?
    # A: Arithmancy and Care of Magical Creatures
#proposal Sylvie
"""

if __name__ == "__main__":
    histogram2()
    #histogram2()
