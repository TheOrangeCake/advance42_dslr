#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import (  # noqa: E402
    import_data,
    get_houses_list,
    get_courses_list,
)

from helper.plot import save_fig  # noqa: E402
coloredlogs.install()

import numpy as np  # noqa: E402

from prepare_data import (  # noqa: E402
    get_binary_labels_for_house,
    init_weights_file,
    save_house_weights,
    select_training_data_features,
    normalize_features,
    save_normalization,
)

#  3 - [OK] Define batch size
# important pour bonus to do sylvie
#      GD: None; mini-batch: 32; SGD: 1;
# BATCH_SIZE = None

"""
    change EPOCH et STEPS
    make train3 ARGS=

    alors il faut regarder la probablité de chaque étudiant pour chaque maison
    et après on choisi 1 maison par étudiant

    ça c'est pour après
    house_prob = []
    for each student
        for house in HOUSES
            probability =
            house_prob.append()

    weights = tableau avec toutes les features(branches) init à zero
    ça va se calculer automatiquement
    les weights c'est ce que le modèle va apprendre
    Il va les utiliser avec des nouvelles datas pour prédire des réponses

    entrainer model:
    données x + vraies réponses y
    calcul des prédictions
    mesure de l'erreur
    modification des weights delta
    répéter
    garder les weights

video
https://www.youtube.com/watch?v=3giTXZbyf1Q
5 functions

Predict function it uses the final values of W and B to compute the final
model's outpt for each training example  returns predicted for each
training example

batch = lot
batch GD = descente de gradient par lots
BATCH_SIZE = None veut dire tout le dataset

epoch         = nombre de passages complets sur le dataset
learning_rate = taille de la modification des weights
step          = une mise à jour des weights
GD, mini-batch et SGD diffèrent ici par le nombre d'exemples utilisés
avant chaque mise à jour des poids.
batch size = None ou nombre total d étudiants:  GD donc on parcourt tout
d un coup le lot c tout les étudiants
batch size = 32 mini batch c est pas petites portions de 32 étudiants
batch size = 1 sdg c'est un par un.

step          = "je modifie les weights une fois"
learning rate = "de combien je les modifie"
"""

COLORS = {
    "Gryffindor": "red",
    "Ravenclaw":  "blue",
    "Hufflepuff": "yellow",
    "Slytherin":  "green",
}

# weight = valeur apprise par le modèle qui indique l’importance et
# l’influence d’une feature sur la prédiction.
# biais = valeur apprise par le modèle .2qui décale la prédiction de
# base, indépendamment des features.
# weight et biais c'est ce que le modèle apprends


def logreg_train(dataset_path, epoch, learning_rate, batch_size):
    print("epochs:", epoch, "learning_rate:", learning_rate)

    # prepare datas
    data = import_data(dataset_path)
    # list of house and courses + verifications
    try:
        list_houses: list[str] = get_houses_list(data)
        list_courses: list[str] = get_courses_list(data)
    except (KeyError, ValueError) as e:
        logging.critical(e)
        sys.exit(1)

    # grades for each student
    training_data_features = select_training_data_features(data)
    # print(training_data_features)

    training_data_features, means, std = normalize_features(
        training_data_features
    )
    for i in range(len(training_data_features)):
        np.set_printoptions(suppress=True, precision=3, linewidth=200)
        # print(training_data_features[i])

# résultats sur lesquels on va venir s entrainer.
    houses_labels = data["Hogwarts House"]
    # print(houses_labels)

    # error type??
# si y a pas autant de réponses que d'étudiants
    if len(training_data_features) != len(houses_labels):
        return
    global nb_training_exmpl
    global nb_input_features

# nb d étudiants avec ses résultats pour s entrainter
    nb_training_exmpl = len(training_data_features)  # nb de lignes
# nb de branches sur lesquells on peut s entrainer.
    nb_input_features = training_data_features.shape[1]  # nb de colonnes

# one-vs-Rest
    # Create history variable to store cost during training
    history = {}
    house_weights = []

    for house in list_houses:
        # PREPARE DATA training_data_labels= LABEL of house = 1
        # other houses = 0
        training_data_labels = get_binary_labels_for_house(
            houses_labels, house
        )
        final_weight, final_biais, cost_history = logistic_regression(
            training_data_features,
            training_data_labels,
            learning_rate,
            epoch, batch_size
        )
        house_weights.append([house, final_biais, *final_weight])
        history[house] = cost_history

    try:
        init_weights_file("weights.csv", list_courses)
        save_house_weights("weights.csv", house_weights)
        save_normalization("weights.csv", means, std)

    except IOError as e:
        logging.critical(e)
        sys.exit(1)

    draw_history(history, epoch, learning_rate, list_houses)
    return


def sigmoid(z) -> float:
    # return float between 0.0 and 1.0 probability
    return 1 / (1 + np.exp(-z))


def cost_function(
    training_data_features, training_data_labels: np.ndarray, weight, biais
):
    # how well how model is doing

    # accumulate the total error across all the training examples
    cost_sum = 0

    # loop over each training exemple
    for i in range(nb_training_exmpl):
        # z = linear combinaton input
        z = np.dot(weight, training_data_features[i]) + biais
        g = sigmoid(z)

        cost_sum += (
            - training_data_labels[i] * np.log(g)
            - (1 - training_data_labels[i]) * np.log(1 - g)
        )
        # return the average cost
    return (1/nb_training_exmpl) * cost_sum


def gradient_function(
    training_data_features, training_data_labels, weight, biais
):
    # compute derivative of the cost function with respect weight and biais
    nb_examples = len(training_data_features)
    # init grad w as a vector
    grad_weight = np.zeros(nb_input_features)
    grad_biais = 0

    for i in range(nb_examples):
        z = np.dot(weight, training_data_features[i]) + biais
        g = sigmoid(z)

        # difference between the output of our model and the true laber Y at I
        grad_biais += (g - training_data_labels[i])
        for j in range(nb_input_features):
            grad_weight[j] += (
                (g - training_data_labels[i]) * training_data_features[i, j]
            )

    grad_biais = (1/nb_examples) * grad_biais
    grad_weight = (1/nb_examples) * grad_weight

    return grad_biais, grad_weight

    # gradient descent


def logistic_regression(
    training_data_features, training_data_labels, alpha, epoch, batch_size
):
    # uses the gradient function to update wheight and bias over a
    # specified number of epoch
    nb_training_data_features = len(training_data_features)
    if batch_size is None:
        batch_size = nb_training_data_features

    weight = np.zeros(nb_input_features)
    biais = 0
    cost_history = []

    for i in range(epoch):
        order = np.random.permutation(nb_training_data_features)
        for start in range(0, nb_training_data_features, batch_size):
            idx = order[start:start + batch_size]
            grad_biais, grad_weight = gradient_function(
                training_data_features[idx],
                training_data_labels[idx],
                weight,
                biais
            )

            weight = weight - alpha * grad_weight
            biais = biais - alpha * grad_biais

        current_cost = cost_function(
            training_data_features, training_data_labels, weight, biais
        )
        if i % 100 == 0:
            print(f"EPOCH {i}: Cost {current_cost}")
        cost_history.append(current_cost)
    return weight, biais, cost_history


def draw_history(
    history: dict[str, list[float]], epoch, learning_rate, list_houses
) -> None:
    for house in list_houses:
        graph.plot(history[house], label=house, color=COLORS[house])
    graph.title(
        f"Training history (step {learning_rate}, {epoch} epochs)"
    )
    graph.xlabel("Epoch")
    graph.ylabel("Cost J(θ)")
    graph.legend()
    graph.grid(alpha=0.3)
    save_fig("model", "training_history.png")
    # graph.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error('Usage: ./logreg_train [Dataset path]')
        sys.exit(1)

    logging.info(f"Logreg Train Dataset source: {sys.argv[1]}")

    try:
        if len(sys.argv) >= 3:
            epoch = int(sys.argv[2])
        else:
            epoch = 1000
        if epoch < 1:
            raise ValueError

        if len(sys.argv) >= 4:
            learning_rate = float(sys.argv[3])
        else:
            learning_rate = 0.01
        if learning_rate <= 0:
            raise ValueError

        if len(sys.argv) >= 5:
            batch_size = int(sys.argv[4])
        else:
            batch_size = None
        if batch_size is not None and batch_size < 1:
            raise ValueError

    except ValueError:
        logging.error(
            'Usage: ./logreg_train.py [Dataset path] '
            'ARGS="<epochs:int> <learning_rate:float> <batch_size:int>"'
        )
        sys.exit(1)

    # learning_rate = STEPS A vérifier
    logreg_train(sys.argv[1], epoch, learning_rate, batch_size)
