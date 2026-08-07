#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
import math
import csv
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
from helper.read_data import read_dataset, is_numeric_column  # noqa: E402
from helper.read_data import read_dataset2

from helper.plot import save_fig  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402
import describe.count_mean_std as cal
coloredlogs.install()

import numpy as np

HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
SKIP = ["Index", "Hogwarts House", "First Name",
        "Last Name", "Birthday", "Best Hand"]
COLORS = {
    "Gryffindor": "red",
    "Ravenclaw":  "blue",
    "Hufflepuff": "yellow",
    "Slytherin":  "green",
}

COURSES = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]



"""
    IMPORT DATA AND CLEAN IT. WICH DATAS?

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

Predict function it uses the final values of W and B to compute the final model's outpt for each training example  returns predicted for each training example

"""    

#X = input data
#nb_training_exmpl = number of training exemple
#nb_input_features = the number of input features
#weight = valeur apprise par le modèle qui indique l’importance et l’influence d’une feature sur la prédiction.
#biais = valeur apprise par le modèle qui décale la prédiction de base, indépendamment des features.
#weight et biais c'est ce que le modèle apprends


def train2():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    data = read_dataset2(sys.argv[1])
    house_col = data.get("Hogwarts House")
    if not house_col:
        logging.critical('Missing or empty "Hogwarts House" column')
        return

    
    #prepare datas
    training_data_features = select_training_data_features(data)
    #print(training_data_features)
    training_data_features, means, std = normalize_features(training_data_features)
#    for i in range(len(training_data_features)):
#        np.set_printoptions(suppress=True, precision=3, linewidth=200)
#        print(training_data_features[i])
    training_data_labels = data["Hogwarts House"]
    #print(training_data_labels)

    # error type??
    if len(training_data_features) !=  len(training_data_labels):
        return
    global nb_training_exmpl 
    global nb_input_features 

    nb_training_exmpl = len(training_data_features) # nb de lignes
    nb_input_features = training_data_features.shape[1] # nb de colonnes

    #itarations = EPOCH.
    if sys.argv == 3:
        iterations = sys.argv[2]
    else:
        iterations = 1000

    #learning_rate = STEPS A vérifier
    if sys.argv == 4:
        learning_rate = sys.argv[3]
    else:
        learning_rate = 0.01
#    for students in nb_training_exmpl:
#        house_score = []
#        for house in HOUSES:

    final_weight, final_biais = logistic_regression(training_data_features, training_data_labels, learning_rate, iterations)

    #put final weight in a file! -> in function main
    return


def sigmoid(z) -> float :
    """return float between 0.0 and 1.0 probability """
    return 1 / (1 + np.exp(-z))

def cost_function(training_data_features, training_data_labels, weight, biais):
    """how well how model is doing"""

     #accumulate the total error across all the training examples
    cost_sum = 0

    #loop over each training exemple
    for i in range(nb_training_exmpl):
        # z = linear combinaton input
        z = np.dot(weight, training_data_features[i]) + biais
        g = sigmoid(z)

        cost_sum += - training_data_labels[i] * np.log(g) - (1 - training_data_labels[i]) * np.log(1 - g)
        #return the average cost
    return (1/nb_training_exmpl) * cost_sum

def gradient_function(training_data_features, training_data_labels, weight, biais):
    """compute derivative of the cost function with respect weight and biais"""

    #init grad w as a vector
    grad_weight = np.zeros(nb_input_features)
    grad_biais = 0

    for i in range(nb_training_exmpl):
        z = np.dot(weight, training_data_features[i]) + biais
        g = sigmoid(z)

        #difference between the output of our model and the true laber Y at I
        grad_biais += (g- training_data_labels[i])
        for j in range(nb_input_features):
            grad_weight[j] += (g - training_data_labels[i]) * training_data_features[i, j]

    grad_biais = (1/nb_training_exmpl) * grad_biais
    grad_weight = (1/nb_training_exmpl) * grad_weight

    return grad_biais, grad_weight

    #gradient descent
def logistic_regression(training_data_features, training_data_labels, alpha, iterations):
    """uses the gradient function to update wheight and bias over a specified number of iterations"""
    weight = np.zeros(nb_input_features)
    biais = 0

    for i in range(iterations):
        grad_biais, grad_weight = gradient_function(training_data_features, training_data_labels, weight, biais)

        weight = weight - alpha * grad_weight
        biais = biais - alpha * grad_biais

        if i % 1000 == 0:
            print(f"Iteration {i}: Cost {cost_function(training_data_features, training_data_labels, weight, biais)}")

    return weight, biais




"""




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
# a refaire....
def normalize_features(features):
    """standardise chaque colonne : (x - moyenne) / écart-type,
    avec les fonctions maison. retourne (features_normalisées, moyennes, ecarts_types)"""

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

# a refaire
def select_training_data_features(data):
    """retourne un tableau [étudiant][note], les valeurs manquantes
    étant remplacées par la médiane de leur colonne (cours)"""

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



if __name__ == "__main__":
    train2()
