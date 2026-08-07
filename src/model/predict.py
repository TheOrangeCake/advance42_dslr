"""
on va reprendre le logre_train

    ça c'est pour après
    house_prob = []
    for each student
        for house in HOUSES
            probability = 
            house_prob.append()
"""

def prediction(data_features, weight, biais):
    """uses the final values of wight and bias to compute the final model's output for each training exemple and return 
       retunr predicted cprobability each training exemple"""
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





if __name__ == "__main__":
    weight, biais = logreg_train(training data,etc...)
    predict()