import csv
import numpy as np
import sys
from helper.read_data import nb_students, get_courses_list, course_data, get_houses_list
import describe.count_mean_std as cal
import math

def get_binary_labels_for_house(houses_labels: list[str], current_house: str) -> np.ndarray:
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

def init_houses_file(path: str) -> None:
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)

        header = ["Index", "Hogwarts House"]
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

def save_student_prediction(
    path: str,
    index: str,
    house: str
) -> None:
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        row = [index, house]
        writer.writerow(row)

def get_iterations() -> int:
    if len(sys.argv) >= 4:
        return int(sys.argv[3])
    return 1000

def get_learning_rate() -> float:
    if len(sys.argv) == 5:
        return float(sys.argv[4])
    return 0.01

#OK
def select_training_data_features(data: dict[str, list[str]])-> np.ndarray:
    #retourne un tableau [étudiant][note], les valeurs manquantes
    #étant remplacées par la médiane de leur colonne (cours)

    grades = []
    course_means = {}
    

    nb_stud = nb_students(data)
    list_course = get_courses_list(data)

    for course in list_course:
        course_means[course] = cal.cal_mean(course_data(data, course))

    for student in range(nb_stud):
        student_grades = []
        for course in list_course:
            grade = data[course][student]
    #        if grade == "nan":
    #            grade = course_means[course]
            student_grades.append(float(grade))
        grades.append(student_grades)

    training_data_features = np.array(grades, dtype=float)
    return training_data_features

#means and stds return for prediction
def normalize_features(features: np.ndarray):
    #valeur normalisée = (value - mean) / std

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
                normalized[i, j]  = 0
            else:
                normalized[i, j]  = (value - means[j]) / stds[j]
    return normalized, means, stds

    





'''
# a refaire....
def normalize_features(features: np.ndarray):
    #standardise chaque colonne : (x - moyenne) / écart-type,
    #avec les fonctions maison. retourne (features_normalisées, moyennes, ecarts_types)

    nb_features = features.shape[1]
    means = np.zeros(nb_features)
    stds = np.zeros(nb_features)
    normalized = np.zeros(features.shape)

    for j in range(nb_features):
        colonne = features[:, j]              # toutes les notes du cours j (numpy)
        valeurs = list(colonne)               # -> liste Python pour tes fonctions

        count = cal.cal_count(valeurs)
        mean = cal.cal_mean(valeurs)
        std = cal.cal_std(valeurs, count, mean)

        if std == 0 or math.isnan(std):       # colonne constante / std invalide -> évite /0
            std = 1

        means[j] = mean
        stds[j] = std
        normalized[:, j] = (colonne - mean) / std

    return normalized, means, stds'''