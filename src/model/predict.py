
from logreg_train import logreg_train, sigmoid
import sys
import logging
from helper.read_data import import_data
from prepare_data import nb_students, init_houses_file, save_student_prediction, select_training_data_features, normalize_features_predict
import numpy as np
from helper.read_data import read_dataset3
"""
TO DO:
PREPARE ALL DATAS

SELECT STUDENT DATAS

PREDICTIONS

SELECTION HOUSE


ordre des courses
means
stds
valeurs utilisées pour remplacer les NaN
weights pour chaque maison
bias pour chaque maison

il faut réutiliser les mêmes processus pour préparer les données que dans le training. 



    return preds

    predictions = predict(X_train, final_w, final_b)
    accuracy = np.mean (prediction == y_train) * 100
    need to bo 98%
    print(f"training accuracy: {accuracy:.2f}%")
    !!! overfitting

"""

def logreg_predict(list_houses, list_courses, means, stds):
    ##uses the final values of wight and bias to compute the final model's output for each training exemple and return 
    ## retunr predicted cprobability each training exemple"""
    if len(sys.argv) < 3:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    #prepare datas:
    grades_data = get_grades_data(list_courses, means, stds)
    nb_stud = grades_data.shape[0]
    houses_biais, houses_weights = read_weights("weights.csv", list_houses, list_courses)
    
    init_houses_file("houses.csv")

    for student in range(nb_stud):
        student_grade = grades_data[student]
        house_prob = np.zeros(len(list_houses))
        for house_index in range(len(list_houses)):
            probability = predict(student_grade, houses_weights[house_index], houses_biais[house_index])
            house_prob[house_index] = probability
        student_prediction = most_probable_house(house_prob, list_houses)
        save_student_prediction("houses.csv",student, student_prediction)
    return

#ok
def get_grades_data(list_courses, means, stds) -> np.ndarray:
    prediction_data = import_data(sys.argv[2])
    students_grades = select_training_data_features(prediction_data)
    ##CHECK IF NB COURSES IN TEST AND TRAIN ARE THE SAME
    students_grades = normalize_features_predict(students_grades, means, stds)
    return students_grades

def read_weights(path: str, list_houses: list[str], list_courses: list[str]) -> tuple[np.ndarray, np.ndarray]:
    houses_biais = np.zeros(len(list_houses))
    houses_weights = np.zeros((len(list_houses), len(list_courses)))
    data = read_dataset3(path)
    for i, house in enumerate(list_houses):

        if house not in data["House"]:
            raise ValueError(f"No weights found for house: {house}")
        row = data["House"].index(house)
        houses_biais[i] = float(data["Bias"][row])
        for j, course in enumerate(list_courses):
            houses_weights[i, j] = float(data[course][row])
    return houses_biais, houses_weights


def most_probable_house(house_prob, list_house):
    chosen_index = 0

    for i in range(len(list_house)):
        if house_prob[i] > house_prob[chosen_index]:
            chosen_index = i

    return list_house[chosen_index]

    
def predict(student_grades: np.array, house_weights: np.array, house_biais: float) -> float: 
    z = np.dot(house_weights, student_grades) + house_biais
    probability = sigmoid(z)
    return float(probability)

if __name__ == "__main__":
    list_houses, list_course, means, stds = logreg_train()
    logreg_predict(list_houses, list_course, means, stds)