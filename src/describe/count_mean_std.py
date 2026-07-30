def cal_count(values: list[float]) -> float:
    if not values:
        return float('nan')
    number = 0
    for value in values:
        if value:
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
            if value is not None:
                occurrences += 1
                total += value
        mean = total / occurrences
    except ZeroDivisionError:
        return float('nan')
    return mean

def cal_std(values: list[float]) -> float:
    if not values:
        return float('nan')
        