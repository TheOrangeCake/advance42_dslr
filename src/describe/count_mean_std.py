def count_occurrences(values: list[float]) -> float:
    if not values:
        return float('nan')
    number = 0
    for l in values:
        if l:
            number += 1
    return number

