#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset  # noqa: E402

coloredlogs.install()


skip = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]


def scatter() -> None:
    if len(sys.argv) != 2:
        logging.critical('Usage: ./scatter [Dataset path]')
        return
    else:
        logging.info(f"Scatter Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])

    out_dir = Path(__file__).resolve().parents[2] / "plots" / "scatter"
    out_dir.mkdir(parents=True, exist_ok=True)

    per_fig = 9
    count = 0
    fig_num = 1
    features = [name for name in data if name not in skip]
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            a = features[i]
            b = features[j]

            x, y = build_axes(data, a, b)

            pos = count % per_fig + 1
            graph.subplot(3, 3, pos)
            graph.scatter(x, y, s=10)
            graph.title(f'{a} vs {b}')
            graph.xlabel(a)
            graph.ylabel(b)
            count += 1
            if (count % per_fig == 0):
                graph.tight_layout()
                graph.savefig(out_dir / f"scatter_{fig_num}.png", dpi=150)
                graph.close()
                fig_num += 1
                graph.figure()
    if count % per_fig != 0:
        graph.tight_layout()
        graph.savefig(out_dir / f"scatter_{fig_num}.png", dpi=150)
        graph.close()
    logging.info(f"Saved {fig_num} plot(s) to {out_dir}")

    print_similar(data, 'Astronomy', 'Defense Against the Dark Arts', out_dir)
    # Conclusion:
    # What are the two features that are similar?
    # Astronomy and Defense Against the Dark Arts


def build_axes(data, a, b):
    x, y = [], []
    for k in range(len(data[a])):
        try:
            xk = float(data[a][k])
            yk = float(data[b][k])
        except ValueError:
            continue
        x.append(xk)
        y.append(yk)
    return x, y


# hardcode af
def print_similar(data, a, b, out_dir):
    logging.info(f"The two most similar features are: {a} and {b}")
    x, y = build_axes(data, a, b)
    graph.figure()
    graph.scatter(x, y)
    graph.title(f'{a} vs {b}')
    graph.xlabel(a)
    graph.ylabel(b)
    graph.tight_layout()
    graph.savefig(out_dir / "similar.png", dpi=150)
    graph.show()


if __name__ == "__main__":
    scatter()
