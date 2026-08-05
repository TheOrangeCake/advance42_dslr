#TO DO SYLVIE

#INDEPENDANT DONC DOIT RELIRE DEPUIS DATASET


#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset2  # noqa: E402
from helper.plot import save_fig  # noqa: E402
from histogram2 import get_data_house_course


HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
COLORS = {
    "Gryffindor": "red",
    "Ravenclaw":  "orange",
    "Hufflepuff": "yellow",
    "Slytherin":  "black",
}
COURSES = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]

def pair_plot():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")
    data = read_dataset2(sys.argv[1])
#    for i in data:
#        print(i, data[i])

    plot = 1
    #loop1 for each feat (course)
    for courseX in COURSES:

        for courseY in COURSES:
            if courseX == courseY:
                pair_histogramm(data, courseX, plot)
            else:
                pair_scatter(data, courseX, courseY)
            #make graph
            plot += 1

    handles, labels = graph.gca().get_legend_handles_labels()
    graph.figlegend(handles, labels, loc='lower right')
    save_fig("histogram2", "histogram2.png")
    #graph.show()
    #afficher graph
    #print(data)

def pair_scatter(data, courseX, couseY):

    return

def pair_histogramm(data, courseX, plot):
    house_scores = {house: [] for house in HOUSES}

    for house in HOUSES:
        house_scores[house] = get_data_house_course(data, house, courseX)
    #build graphics
    graph.subplot(len(COURSES), len(COURSES), plot)
#    graph.xlabel(f"H index: {homogeneity_ind[course]:.3f}")


    for house in HOUSES:
        graph.hist(
            house_scores[house],
            label=house,
            color=COLORS[house],
            alpha=0.5,
            edgecolor='black',
        )
    #graph.title(courseX)
    #handles, labels = graph.gca().get_legend_handles_labels()
    

if __name__ == "__main__":
    pair_plot()