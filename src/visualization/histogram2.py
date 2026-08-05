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

def get_data_house_course(data, house_name, branch):
    values = []

    for i in range(len(data['Hogwarts House'])):
        if data['Hogwarts House'][i] == house_name:
            val = data[branch][i]
            if val is not None and val != ''and val == val:
                values.append(val)
    return values

# calculate the spread of each house mean and std. 
# normalize it to have the same scale
# add it. More the spread of mean and std are large, more the index show it is not homogene
def homogeneity_index(data, course):
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

    #normalize
    mean_spread_norm = mean_spread / dif_max_min
    std_spread_norm = std_spread / dif_max_min

    index = mean_spread_norm + std_spread_norm
    return index

def select_course(homogeneity_ind: dict[str, float]) -> str:
    choosen_course = COURSES[0]
    for course in COURSES:
        if (homogeneity_ind[course] < homogeneity_ind[choosen_course]):
            choosen_course = course
    return choosen_course


def histogram2() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    data = read_dataset2(sys.argv[1])
    house_col = data.get("Hogwarts House")
    #ou ca se trouve dans le fichier de sortie
    if not house_col:
        logging.critical('Missing or empty "Hogwarts House" column')
        return
    plot = 1
    # name = course. plus compréhensible
    homogeneity_ind : dict[str, float] = {}
    for course in COURSES:
        homogeneity_ind[course] = homogeneity_index(data, course)

        #homogeneity_ind[course] = homogeneity_index(data, course)
        house_scores = {house: [] for house in HOUSES}

        for house in HOUSES:
            house_scores[house] = get_data_house_course(data, house, course)
        #build graphics
        graph.subplot(4, 4, plot)
        graph.xlabel(f"H index: {homogeneity_ind[course]:.3f}")
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
    save_fig("histogram2", "histogram2.png")
    #graph.show()
    graph.figure()
    plot = 1
    #display the most homogeneous course
    most_homogeneous_course = select_course(homogeneity_ind)
    house_scores = {house: [] for house in HOUSES}
    for house in HOUSES:
        house_scores[house] = get_data_house_course(data, house, most_homogeneous_course)
        #build graphics
    graph.subplot(1, 1, plot)
    graph.xlabel(f"H index: {homogeneity_ind[most_homogeneous_course]:.3f} , {most_homogeneous_course}")
    #plot += 1
    for house in HOUSES:
        graph.hist(
            house_scores[house],
            label=house,
            color=COLORS[house],
            alpha=0.5,
            edgecolor='black',
        )
    graph.title("most homogeneous course")
    handles, labels = graph.gca().get_legend_handles_labels()
    graph.figlegend(handles, labels, loc='lower right')
    save_fig("histogram2", "Most homogeneous score distribution.png")
    graph.show()



if __name__ == "__main__":
    histogram2()

