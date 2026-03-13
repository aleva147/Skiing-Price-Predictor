import os
import numpy as np
import pandas as pd
from data_functions import *
from model import *
from graph_functions import *
from sklearn.metrics import classification_report
from app_functions import initialize_app



# Csv files paths:
original_data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'offers.csv')
encoded_data_file  = os.path.join(os.path.dirname(__file__), '..', 'data', 'offers_encoded.csv')


# Encode data:
places_map = encode_data(original_data_file, encoded_data_file)

# Load data:
offers_data = pd.read_csv(encoded_data_file)

# Drop irrelevant features.
# offers_data.drop(['id', 'hotel', 'country', 'month', 'num_of_guests'], axis=1, inplace=True)
relevant_cols = ['place', 'date', 'num_of_nights', 'num_of_guests', 'service_type', 'room_size', 'price']  # no negative predictions, but less accurate than with stars feature.
# relevant_cols = ['id', 'hotel', 'country', 'place', 'stars', 'month', 'date', 'num_of_nights', 'num_of_guests', 'service_type', 'room_size']
offers_data = offers_data[relevant_cols]

# Add 'class_id' column to the dataset that indicates the price range the offer is in:
price_ranges = [
    offers_data['price'] <= 500,
    offers_data['price'] <= 1500,
    offers_data['price'] <= 3000,
    offers_data['price'] > 3000,
]
class_names = {
    0: 'Cheapest',
    1: 'Medium',
    2: 'Expensive',
    3: 'Most Expensive'
}
offers_data['class_id'] = np.select(price_ranges, class_names.keys(), default=-1)

# Remove 'price' column:
offers_data.drop(['price'], axis=1, inplace=True)

# Get min and max values for each feature and use it later for normalizing user input in GUI app:
min_place = int(np.amin(offers_data['place']))
max_place = int(np.amax(offers_data['place']))
min_date = int(np.amin(offers_data['date']))
max_date = int(np.amax(offers_data['date']))
min_num_of_nights = int(np.amin(offers_data['num_of_nights']))
max_num_of_nights = int(np.amax(offers_data['num_of_nights']))
min_num_of_guests = int(np.amin(offers_data['num_of_guests']))
max_num_of_guests = int(np.amax(offers_data['num_of_guests']))
min_service_type = int(np.amin(offers_data['service_type']))
max_service_type = int(np.amax(offers_data['service_type']))
min_room_size = int(np.amin(offers_data['room_size']))
max_room_size = int(np.amax(offers_data['room_size']))
normalization_data = [min_place, max_place, min_date, max_date, min_num_of_nights, max_num_of_nights, min_num_of_guests, max_num_of_guests, min_service_type, max_service_type, min_room_size, max_room_size]

# Normalize all columns:
normalized_offers_data = (offers_data - offers_data.min()) / (offers_data.max() - offers_data.min())

# Split data into training and testing datasets: 
data_train, data_test = split_data(normalized_offers_data, 0.2)
X_train = data_train.drop(['class_id'], axis=1).values.tolist()
Y_train = data_train.class_id.values.tolist()
X_test  = data_test.drop(['class_id'], axis=1).values.tolist()
test_trues  = data_test.class_id.values.tolist()

# Initialize KNN model:
model = KNN(X_train, Y_train, k=3)  # Larger k would perform poorly because there are very few 'Cheapest' and 'Most Expensive' offers in comparison to other types. 
# model.calc_k()                    # k = sqrt(len(X)) = 97 gives worse results than when using a small value for k (no 'Cheapest' offers will be recognized for example).
test_preds = model.predict_test_set(X_test)

# Denormalize class_ids (in order to convert them back to class names):
min_class_id = list(class_names.keys())[0]
max_class_id = list(class_names.keys())[-1]
test_trues = [int(min_class_id + val * (max_class_id - min_class_id)) for val in test_trues]
test_preds = [int(min_class_id + val * (max_class_id - min_class_id)) for val in test_preds]

# Test set results:
cnt_correct = 0
for i in range(len(test_trues)):
    if test_preds[i] == test_trues[i]: cnt_correct +=1
print(f"TEST RESULT: Correctly predicted {cnt_correct} samples out of {len(test_trues)} samples in TEST SET.")
print(classification_report(test_trues, test_preds, zero_division=0))

# Confusion matrix:
draw_confusion_matrix(test_trues, test_preds, class_names.values())

# GUI app:
features = relevant_cols[1:-1]  # All features the model uses (remove 'price' column and 'place' column).
print(normalization_data)
initialize_app(model, features, places_map, normalization_data)