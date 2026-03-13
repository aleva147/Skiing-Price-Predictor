from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sborn


def draw_confusion_matrix(trues, preds, class_names):
    matrix = confusion_matrix(trues, preds)
    plt.figure(figsize=(18, 10))
    sborn.heatmap(matrix, xticklabels=class_names, yticklabels=class_names, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted class')
    plt.ylabel('Actual class')
    plt.title('Test Set Confusion Matrix')
    plt.show()