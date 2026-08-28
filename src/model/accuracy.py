import numpy as np
from sklearn.metrics import accuracy_score
from predict import predict
from logreg_train import logreg_train
from predict import logreg_predict
from helper.read_data import read_dataset3
import sys
from helper.prepare_accurary_data import create_accuracy_test_file

def test_accuracy():

    create_accuracy_test_file(sys.argv[1], sys.argv[2])

    list_houses, list_course, means, stds = logreg_train()
    logreg_predict(list_houses, list_course, means, stds)

    predictions_data = read_dataset3("houses.csv")
    y_pred = predictions_data["Hogwarts House"]
    print(y_pred)
    data_train = read_dataset3(sys.argv[1])
    y_true = data_train["Hogwarts House"]

    final_accuracy_score = accuracy_score(y_true, y_pred)
    print("accuracy sklearn: ", final_accuracy_score)


if __name__ == "__main__":
    test_accuracy()