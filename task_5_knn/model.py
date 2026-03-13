import numpy as np
import math
from collections import Counter


class KNN:
    def __init__(self, X, Y, k = 5):
        self.X = X
        self.Y = Y
        self.k = k

    def calc_k(self):
        k = math.floor(math.sqrt(len(self.X)))
        if k % 2 == 0: k += 1
        self.k = k
        print("K = " + str(self.k))

    def predict_test_set(self, X_test):
        predictions = [self.predict_sample(test_sample) for test_sample in X_test]
        return predictions

    def predict_sample(self, sample):
        distances = [self.calc_euclidean_distance(sample, train_sample) for train_sample in self.X]
    
        nearest_neighs_ids = np.argsort(distances)[:self.k]
        nearest_neighs_classes = [self.Y[i] for i in nearest_neighs_ids]
        most_common_class = (Counter(nearest_neighs_classes).most_common(1))[0][0]  # most_common(1) returns a list containing only one element that is a pair of class_type and count.
        return most_common_class

    def calc_euclidean_distance(self, sample1, sample2):
        distance = 0
        for col_sample1, col_sample2 in zip(sample1, sample2):
            distance += (col_sample1 - col_sample2)**2
        return math.sqrt(distance)