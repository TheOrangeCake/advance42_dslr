# See how many values are missing
# Many missing compare Count mean incomplete dataset
def cal_nan_count(values: list[str]) -> float:
    if not values:
        return float('nan')

    count = 0
    for v in values:
        if v == '':
            count += 1
            continue
        try:
            float(v)
        except ValueError:
            count += 1

    return float(count)


# Range can be compared with 25%, 50% and 75% to spot outliners
def cal_range(values: list[float]) -> float:
    if not values:
        return float('nan')
    return values[-1] - values[0]
