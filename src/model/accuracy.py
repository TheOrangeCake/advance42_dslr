from sklearn.metrics import accuracy_score
from logreg_train import logreg_train
from logreg_predict import logreg_predict
from helper.read_data import read_dataset
import sys
from helper.prepare_accurary_data import create_accuracy_test_file
import logging
import csv


def test_accuracy(dataset_train_path, dataset_test_path, iterations, learning_rate):

    logreg_train(dataset_train_path, iterations, learning_rate)
    logreg_predict(dataset_test_path)

    predictions_data = read_dataset("houses.csv")
    y_pred = predictions_data["Hogwarts House"]

    data_train = read_dataset(dataset_train_path)
    y_true = data_train["Hogwarts House"]

    try:
        final_accuracy_score = accuracy_score(y_true, y_pred)
    except ValueError:
        logging.critical("Found input variables with inconsistent numbers of samples")
        sys.exit(1)
    print("accuracy sklearn: ", final_accuracy_score)


if __name__ == "__main__":
#    create_accuracy_test_file(sys.argv[1])
    if len(sys.argv) < 3:
        logging.critical('Usage: ./accuracy [Dataset path] [Datatest path]')
        sys.exit(1)

    logging.info(f"Accuracy Dataset source: {sys.argv[1]}")

    try:
        if len(sys.argv) >= 4:
            iterations =  int(sys.argv[3])
        else:
            iterations = 1000

        if len(sys.argv) >= 5:
            learning_rate = float(sys.argv[4])
        else:
            learning_rate = 0.01

    except ValueError:
        logging.error('Usage: make accuracy ARGS="<iterations:int> <learning_rate:float>"')
        sys.exit(1)

    test_accuracy(sys.argv[1], sys.argv[2], iterations, learning_rate)
