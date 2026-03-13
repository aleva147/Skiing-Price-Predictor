import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
import pandas as pd
from data_functions import encode_date, normalize


def unique_from_column(csv_file, col_id):
    values = set()
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header.
        for row in reader: values.add(row[col_id])
    return sorted(values)

def submit(model, place, entries, places_map, normalization_data):
    date = entries[0].get()
    num_of_nights = int(entries[1].get())
    num_of_guests = int(entries[2].get())
    service_type = entries[3].get()
    room_size = int(entries[4].get())

    # Encode user input:
    encoded_place = places_map[place]
    encoded_date = encode_date(date)
    serv_types = {'najam':1, 'all inclusive':2, 'nocenje s doruckom':3, 'polupansion':4}
    encoded_serv_type = serv_types[service_type]

    # Normalize user input:
    norm_place = normalize(encoded_place, normalization_data[0], normalization_data[1])
    norm_date = normalize(encoded_date, normalization_data[2], normalization_data[3])
    norm_num_of_nights = normalize(num_of_nights, normalization_data[4], normalization_data[5])
    norm_num_of_guests = normalize(num_of_guests, normalization_data[6], normalization_data[7])
    norm_service_type = normalize(encoded_serv_type, normalization_data[8], normalization_data[9])
    norm_room_size = normalize(room_size, normalization_data[10], normalization_data[11])
    # print(f"{norm_place} {norm_date} {norm_num_of_nights} {norm_num_of_guests} {norm_service_type} {norm_room_size}")
    
    # Predict price:
    sample = [norm_place, norm_date, norm_num_of_nights, norm_num_of_guests, norm_service_type, norm_room_size]
    pred = model.predict_single_input(sample)
    
    # Denormalize predicted price:
    price_min = normalization_data[12]
    price_max = normalization_data[13]
    pred = price_min + pred * (price_max - price_min)
    print(f"Predicted price: {pred}")
    messagebox.showinfo("Predicted price", pred)


def initialize_app(model, features, places_map, normalization_data):
    # Load destinations from a CSV file:
    offers_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'offers.csv')
    places_dropdown = unique_from_column(offers_csv, 2)


    # Create main window
    root = tk.Tk()
    root.title("Price Predictor")

    # Dropdown label and combobox
    tk.Label(root, text="place:").grid(row=0, column=0, padx=10, pady=5)
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=dropdown_var)
    dropdown['values'] = places_dropdown
    dropdown.current(0)
    dropdown.grid(row=0, column=1, padx=10, pady=5)

    # Input fields for other features:
    entries = []
    for i in range(len(features)):
        label = tk.Label(root, text=f"{features[i]}:")
        label.grid(row=i+1, column=0, padx=10, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=i+1, column=1, padx=10, pady=5)
        entries.append(entry)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: submit(model, dropdown_var.get(), entries, places_map, normalization_data))
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()