
from logreg_train3 import logreg_train
import sys
import logging
from helper.read_data import import_data
from prepare_data import nb_students, init_houses_file, save_student_prediction
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

    preds = np.zeros(nb_training_exmpl)

    for i in range(nb_training_exmpl):
        z = np.dot(weight, training_data_features[i]) + biais
        g = sigmoid(z)

        preds[i] = g

    return preds

    predictions = predict(X_train, final_w, final_b)
    accuracy = np.mean (prediction == y_train) * 100
    need to bo 98%
    print(f"training accuracy: {accuracy:.2f}%")
    !!! overfitting

"""

def logreg_predict(list_houses, means, stds):
    ##uses the final values of wight and bias to compute the final model's output for each training exemple and return 
    ## retunr predicted cprobability each training exemple"""
    if len(sys.argv) < 2:
        logging.critical('Usage: ./histogram [Dataset path]')
        return
    else:
        logging.info(f"Histogram Dataset source: {sys.argv[1]}")

    #prepare datas:
    prediction_data = import_data(sys.argv[2])
    #see if values = nan??
    nb_stud = nb_students(prediction_data)
    house_prob = []
    index = 0
    init_houses_file("houses.csv")

    #import weights and bias
    #use stds and means
    #list_course???
    print("nb stud: ", nb_stud)

    for student in range(nb_stud):
        #student_data = get_student_prediction_data(prediction_data)
        for house in list_houses:
            continue
            #probability = prediction(house, ....)
            #house_prob[].append(probability)
        #chosen_house = 
        #house_prob.empty()
        save_student_prediction("houses.csv",index, "Herbert")
        index += 1
    return
'''
def get_student_prediction_data(prediction_data):

def most_probable_house(house_prob, list_house):
    chosen_house = 0
    for i in list_house:
        if house_prob[i] > chosen_house:
            chosen_house = i

    chosen_house = max_house

def prediction():
    #algo important. 

'''
if __name__ == "__main__":
    list_houses, means, stds = logreg_train()
    logreg_predict(list_houses, means, stds)