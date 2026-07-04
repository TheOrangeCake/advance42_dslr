import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from helper.models import Feature  # noqa: E402

display_name = {
    'count': 'Count',
    'mean': 'Mean',
    'std': 'Std',
    'min': 'Min',
    'quarter': '25%',
    'half': '50%',
    'three_quarter': '75%',
    'max': 'Max'
}


def display(features: list[Feature]) -> None:
    if not features:
        return

    spacing = "    "

    col_len: list[int] = []
    col_len.append(max(len(label) for label in display_name.values()))
    for feature in features:
        w = len(feature.name)
        for attr in display_name:
            v = getattr(feature, attr, None)
            if v is not None:
                w = max(w, len(f"{v:.6f}"))
        col_len.append(w)

    print(f"{'':<{col_len[0]}}", end="")
    for index, feature in enumerate(features):
        print(f"{spacing}{feature.name:>{col_len[index + 1]}}", end="")
    print()

    for attr, label in display_name.items():
        values = [getattr(feature, attr, None) for feature in features]
        if any(v is None for v in values):
            continue
        print(f"{label:<{col_len[0]}}", end="")
        for index, v in enumerate(values):
            print(f"{spacing}{v:>{col_len[index + 1]}.6f}", end="")
        print()
