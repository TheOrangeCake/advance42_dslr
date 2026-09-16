from sklearn.metrics import accuracy_score
from logreg_train import logreg_train
from logreg_predict import logreg_predict
from helper.read_data import read_dataset
import sys
from helper.prepare_accurary_data import create_accuracy_test_file
import logging


def test_accuracy(dataset_train_path, dataset_test_path):

    create_accuracy_test_file(sys.argv[1])

    logreg_train(dataset_train_path)
    logreg_predict(dataset_test_path)

    predictions_data = read_dataset("houses.csv")
    y_pred = predictions_data["Hogwarts House"]
    # print(y_pred)
    data_train = read_dataset(sys.argv[2])
    y_true = data_train["Hogwarts House"]

    final_accuracy_score = accuracy_score(y_true, y_pred)
    print("accuracy sklearn: ", final_accuracy_score)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.critical('Usage: ./accuracy [Dataset path]')
        sys.exit(1)

    logging.info(f"Accuracy Dataset source: {sys.argv[1]}, {sys.argv[2]}")
    test_accuracy({sys.argv[1]}, {sys.argv[2]})
