import csv
import numpy as np
import sys
from helper.read_data import nb_students, get_courses_list, course_data
import describe.count_mean_std as cal


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

def get_iterations() -> int:
    if len(sys.argv) == 3:
        return int(sys.argv[2])
    return 1000

def get_learning_rate() -> float:
    if len(sys.argv) == 4:
        return int(sys.argv[3])
    return 0.01


# a refaire

def select_training_data_features(data):
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
            if grade == "nan":
                grade = course_means[course]
            student_grades.append(float(grade))
        grades.append(student_grades)

    training_data_features = np.array(grades, dtype=float)

    return training_data_features


"""
def select_training_data_features(data):
    #retourne un tableau [étudiant][note], les valeurs manquantes
    #étant remplacées par la médiane de leur colonne (cours)

    # 1. on garde les colonnes qui sont des features (pas dans SKIP)
    feature_cols = [col for col in data if col not in SKIP]

    # 2. on construit chaque colonne nettoyée
    cleaned_cols = []
    for col in feature_cols:
        # tableau float avec np.nan à la place des None
        colonne = np.array(
            [np.nan if v is None else float(v) for v in data[col]],
            dtype=float,
        )
        #!!! mean c'est pas median!!
        col_median = cal.cal_mean(colonne)
        # on bouche les trous avec cette médiane
        colonne[np.isnan(colonne)] = col_median
        cleaned_cols.append(colonne)

    # 3. cleaned_cols est orienté colonnes -> .T pour passer en [étudiant][note]
    training_data_features = np.array(cleaned_cols).T

    return training_data_features

# a refaire....
def normalize_features(features):
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

    return normalized, means, stds


def select_training_data_features(data):

    selected_courses = [col for col in data if col in COURSES]

    nb_students = len(data[selected_courses[0]])

    print(selected_courses)
    print(COURSES)

    rows = []
    for i in range(nb_students):
        row = [data[col][i] for col in selected_courses]
        rows.append(row)

    #normalized

    return np.array(rows)

"""