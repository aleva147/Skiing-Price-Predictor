import numpy as np
import math


class LinearRegressionModel:
    def __init__(self, learning_rate = 0.01, n_iters=10000):
        self.learning_rate = learning_rate  # this is alpha in mathematical formulas.
        self.n_iters = n_iters
        self.weights = None
        self.bias = None


    # Train model:
    #   X: 2D vector containing multiple different requests (table rows) at once, for a more efficient code, and all feature values within each request. 
    #  (e.g. X=[['Italija', 'Torino', '2 stars'... ], ['Francuska', 'Val d'Isere', '3 stars'... ], ...], except that, of course, these strings will be encoded to numerical values instead beforehand)
    def fit(self, X, y):
        n_samples, n_features = X.shape  # Numpy .shape method returns all dimensions of a vector/matrix. 
        # Initial values for all weights and for bias are zero:
        self.weights = np.zeros(n_features)
        self.bias    = 0

        for i in range(self.n_iters):
            if i % 1000 == 0: 
                print(f"Iteration: {i} / {self.n_iters}")
                print(f"\tWeights and bias: {self.weights}, {self.bias}")

            h = np.dot(X, self.weights) + self.bias  # Formula: y = wx + b 

            dw = (2/n_samples) * np.dot(X.T, (h-y))  # Formula: 1/N * sum(2*x_i*(y_correct - y_i)), np.dot calculates all x_i at the same time (sum is performed by default). It was only important to transpose the X matrix first so that it can be multiplied with dy vector.
            db = (2/n_samples) * np.sum(h-y)         # Formula: 1/N * sum(2*(y_correct - y_i)).

            self.weights = self.weights - self.learning_rate * dw  # Formula: w = w - alpha*dw. By calculating all new weights at the same time, we are performing "group gradient descent", and not "stochastic gradient descent". 
            self.bias    = self.bias - self.learning_rate * db        # Formula: b = b - alpha*db.

        print(f"Iteration: {self.n_iters} / {self.n_iters}")
        print(f"\tBias and weights: {self.bias}, {self.weights}")
            

    # Predicts a price for any new X by always using the weights and bias it has calculated after all the training has been complete:
    def predict(self, X):
        y_pred = np.dot(X, self.weights) + self.bias
        return y_pred

    # Predicts a price for the encoded and normalized user input from the GUI app:  
    def predict_single_input(self, x):
        pred = 0
        for feature, weight in zip(x, self.weights):
            pred += feature * weight
        pred += self.bias
        return pred


    # Calculate RMSE:
    def root_mean_squared_error(self, y_true, y_pred):
        return math.sqrt(np.sum((y_true - y_pred)**2) / (2*len(y_true)))