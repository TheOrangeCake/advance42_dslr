import csv
import numpy as np
import sys
import logging
from helper.read_data import (
    nb_students,
    get_courses_list,
    course_data,
    read_dataset,
)
import describe.count_mean_std as cal


def get_binary_labels_for_house(
    houses_labels: list[str], current_house: str
) -> np.ndarray:
    training_data_labels = np.zeros(len(houses_labels), dtype=int)
    for i in range(len(houses_labels)):
        if houses_labels[i] == current_house:
            training_data_labels[i] = 1
    return training_data_labels


def init_weights_file(path: str, courses: list[str]) -> None:
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)

        header = ["House", "Bias"] + courses
        writer.writerow(header)

def save_house_weights(
    path: str,
    house: str,
    bias: float,
    weights: np.ndarray
) -> None:
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)

        row = [house, bias] + weights.tolist()
        writer.writerow(row)


def save_students_predictions(
    path: str,
    students_predictions: list[str]
) -> None:
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Hogwarts House"])
        for index, house in enumerate(students_predictions):
            writer.writerow([index, house])


# OK arrah student course.
def select_training_data_features(data: dict[str, list[str]]) -> np.ndarray:
    # retourne un tableau [étudiant][note],
    grades = []

    try:
        nb_stud = nb_students(data)
        list_courses = get_courses_list(data)
    except (KeyError, ValueError) as e:
        logging.critical(e)
        sys.exit(1) 

    for student in range(nb_stud):
        student_grades = []
        for course in list_courses:
            grade = data[course][student]
            student_grades.append(float(grade))
        grades.append(student_grades)

    training_data_features = np.array(grades, dtype=float)
    return training_data_features


# means and stds return for prediction
def normalize_features(features: np.ndarray):
    # valeur normalisée = (value - mean) / std

    nb_features = features.shape[1]
    normalized = np.zeros(features.shape)
    means = np.zeros(nb_features)
    stds = np.zeros(nb_features)

    for j in range(features.shape[1]):
        branch_column = features[:, j]
        branch_values = branch_column.tolist()
        means[j] = cal.cal_mean(branch_values)
        count = cal.cal_count(branch_values)
        stds[j] = cal.cal_std(branch_values, count, means[j])
        if stds[j] == 0 or np.isnan(stds[j]):
            normalized[:, j] = 0
            continue
        for i in range(features.shape[0]):
            value = features[i, j]
            if np.isnan(value):
                normalized[i, j] = 0
            else:
                normalized[i, j] = (value - means[j]) / stds[j]
    return normalized, means, stds


def normalize_features_predict(features: np.ndarray, means, stds):
    # valeur normalisée = (value - mean) / std

    normalized = np.zeros(features.shape)

    for j in range(features.shape[1]):

        if stds[j] == 0 or np.isnan(stds[j]):
            normalized[:, j] = 0
            continue
        for i in range(features.shape[0]):
            value = features[i, j]
            if np.isnan(value):
                normalized[i, j] = 0
            else:
                normalized[i, j] = (value - means[j]) / stds[j]
    return normalized


def save_normalization(
    path: str, courses: list[str], means: np.ndarray, stds: np.ndarray
) -> None:
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Course", "Mean", "Std"])
        for course, mean, std in zip(courses, means, stds):
            writer.writerow([course, mean, std])


def read_normalization(path: str) -> tuple[list[str], np.ndarray, np.ndarray]:
    data = read_dataset(path)
    means = np.array(data["Mean"], dtype=float)
    stds = np.array(data["Std"], dtype=float)
    return means, stds


def read_weights(
    path: str,
) -> tuple[list[str], list[str], np.ndarray, np.ndarray]:
    data = read_dataset(path)
    list_houses = data["House"]
    list_courses = [c for c in data if c not in ("House", "Bias")]
    houses_biais = np.array(data["Bias"], dtype=float)
    houses_weights = np.zeros((len(list_houses), len(list_courses)))
    for i in range(len(list_houses)):
        for j, course in enumerate(list_courses):
            houses_weights[i, j] = float(data[course][i])
    return list_houses, list_courses, houses_biais, houses_weights
