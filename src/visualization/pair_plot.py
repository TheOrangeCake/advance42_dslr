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
    graph.xlabel("graphic")
    
    #loop1 for each feat (course)
    for courseX in COURSES:
        graph.xticks(ticks=courseX)
        for courseY in COURSES:
            if courseX == courseY:
                pair_histogramm(data, courseX, plot)
            else:
                pair_scatter(data, courseX, courseY)
            #make graph
            plot += 1

                
            #titre des axes
            #graph.xlabel(a)
            #graph.ylabel(b)
    
    handles, labels = graph.gca().get_legend_handles_labels()

    graph.figlegend(handles, labels, loc='lower right')
    for ax in graph.gcf().get_axes():
        ax.set_xticks([])
        ax.set_yticks([])
    #graph.title(f'pair_plot22') on met pas....
    #créer le fichier
    save_fig("pair_plot", "pair_plot.png")
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
    ax = graph.subplot(len(COURSES), len(COURSES), plot)
    #ax.set_xticks([])
    #ax.set_yticks([])
    #graph.subplot(len(COURSES), len(COURSES), plot)
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


"""
    # scatter = dispersion
    def scatter() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./scatter [Dataset path]')
        return
    else:
        logging.info(f"Scatter Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])

    per_fig = 9
    count = 0
    fig_num = 1
    features = [name for name in data if name not in SKIP]
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            #chaque branche
            a = features[i]
            b = features[j]

            #ai pas encore compris
            x, y = build_axes(data, a, b)

            # pas compris
            pos = count % per_fig + 1

            # ok il a mis 3 x 3 mais moi je vais mettre genre 13  x 13. Le nombre de course
            graph.subplot(3, 3, pos)
            #rajouter couleur x,y c'est les données, s c'est la taille du point. on va rajouer color

            graph.scatter(x, y, s=10)
            # pour mettre le titre. Mais attention nous on doit mettre le titre en haut et de coté.
            #titre de chaque graphique
            graph.title(f'{a} vs {b}')
            #titre des axes
            graph.xlabel(a)
            graph.ylabel(b)
            count += 1
            if (count % per_fig == 0):
                save_fig("scatter", f"scatter_{fig_num}.png")
                graph.close()
                fig_num += 1
                graph.figure()
    if count % per_fig != 0:
        save_fig("scatter", f"scatter_{fig_num}.png")
        graph.close()
"""