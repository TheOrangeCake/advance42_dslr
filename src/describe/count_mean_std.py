import math 

def cal_count(values: list[float]) -> int:
    number = 0
    for value in values:
        if value is not None and not math.isnan(value):
            number += 1
    return number

#The arithmetic mean is the sum of the data divided by the number of data points.
def cal_mean(values: list[float]) -> float:
    if not values:
        return float('nan')
    occurrences = 0
    total = 0
    try:
        for value in values:
            if value is not None and not math.isnan(value):
                occurrences += 1
                total += value
        mean = total / occurrences
    except ZeroDivisionError:
        return float('nan')
    return mean

#standard deviation
def cal_std(values: list[float], count:int, mean: float) -> float:
    if not values or  count < 2:
        return float('nan')
    squared_differences = 0.0
    for value in values:
        if value is not None and not math.isnan(value):
            squared_differences += (value - mean) ** 2
    standard_deviation = math.sqrt((squared_differences / (count - 1)))
    return (standard_deviation)

def diff_max_min(values: list[float]) -> float:
    max = float('-inf')
    min = float('inf')
    for value in values:
        if value is not None and not math.isnan(value) and value > max:
            max = value
        if value is not None and not math.isnan(value) and value < min:
            min = value
        else:
            continue
    if max == float('-inf') or min == float('inf'):
        return float('nan')
    return (max-min)