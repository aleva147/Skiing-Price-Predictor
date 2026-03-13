import matplotlib.pyplot as plt
import numpy as np


# Draw a scatter plots to illustrate the effects of a single feature on prices:
def draw_feature_scatter_plot(feature_name, feature_col, price_col):
    plt.figure(figsize=(18, 10))
    plt.title(f'Prices depending on {feature_name}')
    plt.xlabel(feature_name)
    plt.ylabel('price')

    plt.scatter(feature_col, price_col, alpha=0.8, color='orange', label='Price')

    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


# Draw a scatter plot to show how accurate the predicted prices are in comparison to actual prices:
def draw_predicted_vs_actual_plot(title, pred, actual):
    plt.figure(figsize=(18, 10))
    plt.title(title)
    plt.xlabel('SAMPLE ID')
    plt.ylabel('PRICE')

    samples_cnt = len(actual)
    sample_ids = np.arange(1, samples_cnt + 1)
    plt.scatter(sample_ids, actual, alpha=0.8, color='green', label="Actual price")
    plt.scatter(sample_ids, pred, alpha=0.8, color='orange', label="Predicted price")
    
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()