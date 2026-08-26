#!/usr/bin/env python3
import matplotlib.pyplot as graph
import sys
import logging
import math
import csv
from pathlib import Path
import coloredlogs
sys.path.append(str(Path(__file__).parent.parent))
#from helper.read_data import read_dataset, is_numeric_column  # noqa: E402
from helper.read_data import read_dataset3, get_houses_list, get_courses_list

from helper.plot import save_fig  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402
import describe.count_mean_std as cal
coloredlogs.install()

import numpy as np

from prepare_data import get_binary_labels_for_house, init_weights_file, save_house_weights, get_iterations, get_learning_rate, select_training_data_features

## on va effacer
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


def train3():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    #itarations = EPOCH.
    iterations = get_iterations()

    #learning_rate = STEPS A vérifier
    learning_rate = get_learning_rate()

    #prepare datas
    data = read_dataset3(sys.argv[1])
    ## list of house and courses + verifications
    list_houses: list[str] = get_houses_list(data)
    if not list_houses:
        logging.critical('Missing or empty "Hogwarts House" column')
        return
    #print(list_houses)
    list_courses: list[str] = get_courses_list(data)
    #print(list_courses)

    #grades for each student
    training_data_features = select_training_data_features(data)
    #print(training_data_features)
    
 #   training_data_features, means, std = normalize_features(training_data_features)
    for i in range(len(training_data_features)):
        np.set_printoptions(suppress=True, precision=3, linewidth=200)
        print(training_data_features[i])
    return
    """

##résultats sur lesquels on va venir s entrainer. 
    houses_labels = data["Hogwarts House"]
    #print(houses_labels)

    # error type??
## si y a pas autant de réponses que d'étudiants
    if len(training_data_features) !=  len(houses_labels):
        return
    global nb_training_exmpl 
    global nb_input_features 

##nb d étudiants avec ses résultats pour s entrainter
    nb_training_exmpl = len(training_data_features) # nb de lignes
##nb de branches sur lesquells on peut s entrainer. 
    nb_input_features = training_data_features.shape[1] # nb de colonnes

## one-vs-Rest
    init_weights_file("weights.csv", list_courses)
    for house in list_houses:
        ##PREPARE DATA training_data_labels= LABEL of house = 1 other houses = 0
        training_data_labels = get_binary_labels_for_house(houses_labels, house)
        final_weight, final_biais = logistic_regression(training_data_features, training_data_labels, learning_rate, iterations)
        save_house_weights("weights.csv", house, final_biais, final_weight)
"""
    
    


"""
def sigmoid(z) -> float :
    #return float between 0.0 and 1.0 probability
    return 1 / (1 + np.exp(-z))

def cost_function(training_data_features, training_data_labels: int, weight, biais):
    #how well how model is doing

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
    #compute derivative of the cost function with respect weight and biais

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
    #uses the gradient function to update wheight and bias over a specified number of iterations
    return 1,2
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



if __name__ == "__main__":
    train3()
