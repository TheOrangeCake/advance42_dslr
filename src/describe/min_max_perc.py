from math import floor

#calculs pour make describe
def cal_min(values: list[float]) -> float:
    if not values:
        return float('nan')
    return values[0]


def cal_max(values: list[float]) -> float:
    if not values:
        return float('nan')
    return values[-1]


def cal_per(values: list[float], p: int) -> float:
    if not values:
        return float('nan')
    if p < 0 or p > 100:
        return float('nan')

    position = (len(values) - 1) * p / 100
    lower = floor(position)
    diff = position - lower
    if diff == 0:
        return values[lower]
    return values[lower] + diff * (values[lower + 1] - values[lower])
