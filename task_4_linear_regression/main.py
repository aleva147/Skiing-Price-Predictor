import os
import numpy as np
import pandas as pd
from data_functions import *
from model import *
from graph_functions import *
from app_functions import *


# Csv files paths:
original_data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'offers.csv')
encoded_data_file  = os.path.join(os.path.dirname(__file__), '..', 'data', 'offers_encoded.csv')


# Encode data:
places_map = encode_data(original_data_file, encoded_data_file)

# Load data:
offers_data = pd.read_csv(encoded_data_file)

# Drop irrelevant features:
relevant_cols = ['place', 'date', 'num_of_nights', 'num_of_guests', 'service_type', 'room_size', 'price']  # no negative predictions, but less accurate than with stars feature.
# relevant_cols = ['id', 'hotel', 'country', 'place', 'stars', 'month', 'date', 'num_of_nights', 'num_of_guests', 'service_type', 'room_size']
offers_data = offers_data[relevant_cols]

# # Draw scatter plots to illustrate the effects of each feature on prices:
# for column_name in offers_data.columns:
#     if column_name == 'price': continue
#     draw_feature_scatter_plot(column_name, offers_data[column_name], offers_data['price'])

# Save the min and max price (used for later denormalization when displaying graphs and calculating RMSE):
min_price = np.amin(offers_data['price'])
max_price = np.amax(offers_data['price'])
# Save the min and max values for each feature (used for later normalization of user input in the GUI app):
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
normalization_data = [min_place, max_place, min_date, max_date, min_num_of_nights, max_num_of_nights, min_num_of_guests, max_num_of_guests, min_service_type, max_service_type, min_room_size, max_room_size, int(min_price), int(max_price)]

# Normalize all columns:
normalized_offers_data = (offers_data - offers_data.min()) / (offers_data.max() - offers_data.min())

# Split data into training and testing datasets: 
data_train, data_test = split_data(normalized_offers_data, 0.2)
X_train = data_train.drop(['price'], axis=1)
Y_train = data_train.price
X_test  = data_test.drop(['price'], axis=1)
Y_test  = data_test.price

# Train model:
model = LinearRegressionModel(learning_rate=0.01, n_iters=10000)
model.fit(X_train, Y_train)


# Evaluate model on the train set:
train_preds = model.predict(X_train)
train_preds = denormalize(train_preds, min_price, max_price)
# train_preds = [max(400.0, val) for val in train_preds]
train_trues = denormalize(Y_train, min_price, max_price)
rmse_train = model.root_mean_squared_error(train_trues, train_preds)
print(f"Train set RMSE: {rmse_train:.2f}")
draw_predicted_vs_actual_plot('Comparing predicted and actual prices on the TRAIN SET', train_preds, train_trues)

# Evaluate model on the test set:
test_preds = model.predict(X_test)
test_preds = denormalize(test_preds, min_price, max_price)
# test_preds = [max(400.0, val) for val in test_preds]
test_trues = denormalize(Y_test, min_price, max_price)
rmse_test = model.root_mean_squared_error(test_trues, test_preds)
print(f"Test set RMSE: {rmse_test:.2f}")
draw_predicted_vs_actual_plot('Comparing predicted and actual prices on the TEST SET', test_preds, test_trues)

# Debug:
for i in range(len(train_preds)):
    if (train_preds[i] < 0):  print(f"NEGATIVE PREDICTION (TRAIN): {train_preds[i]}, ACTUAL VALUE: {list(train_trues)[i]}")
for i in range(len(test_preds)):
    if (test_preds[i] < 0): print(f"NEGATIVE PREDICTION (TEST): {test_preds[i]}, ACTUAL VALUE: {list(test_trues)[i]}")


# GUI app:
features = relevant_cols[1:-1]  # All features the model uses (remove 'price' column and 'place' column).
# print(normalization_data)
initialize_app(model, features, places_map, normalization_data)