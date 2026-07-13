#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402

coloredlogs.install()


houses = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
skip = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
house_colors = {
    "Gryffindor": "red",
    "Ravenclaw":  "blue",
    "Hufflepuff": "yellow",
    "Slytherin":  "green",
}


def histogram() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])
    house_col = data.get("Hogwarts House")
    plot = 1
    for name, values in data.items():
        if name in skip:
            continue
        house_scores = {house: [] for house in houses}
        for i in range(len(house_col)):
            try:
                score = float(values[i])
            except ValueError:
                continue
            house_scores[house_col[i]].append(score)
        graph.subplot(4, 4, plot)
        plot += 1
        for house in houses:
            graph.hist(
                house_scores[house],
                label=house,
                color=house_colors[house],
                alpha=0.5,
                edgecolor='black',
            )
        graph.title(name)
    handles, labels = graph.gca().get_legend_handles_labels()
    graph.figlegend(handles, labels, loc='lower right')
    graph.tight_layout()
    graph.show()
    # Conclusion:
    # Which Hogwarts course has a homogeneous score
    # distribution between all four houses?
    # Arithmancy and Care of Magical Creatures


if __name__ == "__main__":
    histogram()
