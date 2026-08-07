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
from helper.plot import save_fig  # noqa: E402
from describe.min_max_perc import cal_min, cal_max  # noqa: E402

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

def train2():
    if len(sys.argv) != 2:
        logging.critical('Usage: ./logreg_train [Dataset path]')
        return
    else:
        logging.info(f"Logreg_train Dataset source: {sys.argv[1]}")

    data = read_dataset(sys.argv[1])
    print("ciao")


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
sigmoid:
take a linear combination input C and return our probability output between 0 and 1
cost function: compute how well our model is doing
derivative function: compute derivative of the cost function with respect W and B
gradient descent fucntion to update our parameters W and B over a specified number of iterations
Predict function it uses the final values of W and B to compute the final model's outpt for each training example  returns predicted for each training example

"""    

#X = input data
#nb_training_exmpl = number of training exemple
#nb_input_features = the number of input features
#weight = valeur apprise par le modèle qui indique l’importance et l’influence d’une feature sur la prédiction.
#biais = valeur apprise par le modèle qui décale la prédiction de base, indépendamment des features.
#weight et biais c'est ce que le modèle apprends
def train2():
    #prepare datas
    # read data
    #select features
    # X = data sans les titres...
    #nb_training_exmpl = cal.cal_count(data) blabla...
    #nb_input feature = nb row or col...
    #itaration = EPOCH. A voir avec argv à voir...

    #function logreg
    return
    
C'est quoi le y?

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost_function(training_data, y, weight,biais):
    cost_sum = 0

    for i in range(nb_training_exmpl):
        z = np.dot(weight, training_data[i]) + biais
        g= sigmoid(z)

        cost_sum += -y[i] * np.log(g) - (1 -y[i]) * np.log(1 - g)
        #return the average cost
    return (1/nb_training_exmpl) * cost_sum

def gradient_function(training_data, y, weight, biais):
    grad_w = np.zeros(nb_input_features)
    grad_b = 0

    for i in range(nb_training_exmpl):
        z = np.dot(weight, training_data[i]) + biais
        g = sigmoid(z)

        #difference between the output of our model and the true laber Y at I
        grad_b += (g- y[i])
        for j in range(nb_input_features):
            grad_w[j] += (g - y[i]) *training_data[i, j]

    grad_b = (1/nb_training_exmpl) * grad_b
    grad_w = (1/nb_training_exmpl) * grad_w

    return grad_b, grad_w


def gradient_descent(training_data, y, alpha, iterations):
    weight = np.zeros(nb_input_features)
    biais = 0

    for i in range(iterations):
        grad_b, grad_w = gradient_function(training_data, y, weight, biais)

        weight = weight - alpha * grad_w
        b = b - alpha * grad_b

        if i % 1000 == 0:
            print(f"Iteration {i}: Cost {cost_function(training_data, y, weight, biais)}")

    return weight, biais


#for nexte excercie?
def prediction(training_data, weight, biais):
    preds = np.zeros(nb_training_exmpl)

    for i in range(nb_training_exmpl):
        z = np.dot(weight, training_data[i]) + biais
        g = sigmoid(z)

        preds[i] = g

    return preds


exemple:
    learning_rate = 0.01
    itarations = 1000

    final_w, final_b = gradient_descent(X_train, learning_rate, iterations)

    predictions = predict(X_train, final_w, final_b)
    accuracy = np.mean (prediction == y_train) * 100
    need to bo 98%
    print(f"training accuracy: {accuracy:.2f}%")
    !!! overfitting


if __name__ == "__main__":
    train2()