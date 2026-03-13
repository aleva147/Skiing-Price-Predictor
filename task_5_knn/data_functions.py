import csv


# Create an encoded csv file from the original csv:
def encode_data(input_csv_file, output_csv_file):
    # Map the names of months to numeric values:
    months = {'Dec':0, 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4}
    # Map the names of service types to numeric values:
    serv_types = {'najam':1, 'all inclusive':2, 'nocenje s doruckom':3, 'polupansion':4}
    # Map the names of countries and places to numeric values:
    country_id = 1
    seen_countries = {}
    place_id = 1
    seen_places = {}

    with open(input_csv_file, mode='r', newline='', encoding='utf-8') as org_file, \
        open(output_csv_file, mode='w', newline='', encoding='utf-8') as enc_file:
        
        reader = csv.DictReader(org_file)

        writer = csv.DictWriter(enc_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Read original data row by row and encode country, place, month and service type names, 
        #  remove euro symbol from prices and ' m2' from room sizes, and convert date to the overall week id
        #  (week 1 is for dates between 01.11. and 07.11. and week 24 is for dates between 23.04. and 30.04. 
        for row in reader:
            # Country field:
            country = row['country']
            if country not in seen_countries:
                seen_countries[country] = country_id
                country_id += 1
            row['country'] = seen_countries[country]
            
            # Place field:
            place = row['place']
            if place not in seen_places:
                seen_places[place] = place_id
                place_id += 1
            row['place'] = seen_places[place]
                
            # Month field:
            row['month'] = months[row['month']]

            # Date field:
            date_parts = row['date'].split('.')
            day = int(date_parts[0])
            week = 0
            if day < 8:     week = 1
            elif day < 16:  week = 2
            elif day < 23:  week = 3
            else:           week = 4

            month = int(date_parts[1])
            if month == 11:   month = 0
            elif month == 12: month = 1
            elif month == 1:  month = 2
            elif month == 2:  month = 3
            elif month == 3:  month = 4
            elif month == 4:  month = 5

            row['date'] = week + 4 * month

            # Service type:
            row['service_type'] = serv_types[row['service_type']]
            
            # Room size:
            row['room_size'] = row['room_size'][:-3]
            
            # Price
            row['price'] = row['price'][:-1]

            writer.writerow(row)

    return seen_places


def encode_date(date_str):
    date_parts = date_str.split('.')

    day = int(date_parts[0])
    week = 0
    if day < 8:     week = 1
    elif day < 16:  week = 2
    elif day < 23:  week = 3
    else:           week = 4

    month = int(date_parts[1])
    if month == 11:   month = 0
    elif month == 12: month = 1
    elif month == 1:  month = 2
    elif month == 2:  month = 3
    elif month == 3:  month = 4
    elif month == 4:  month = 5

    return week + 4 * month


def normalize(val, val_min, val_max):
    return (val - val_min) / (val_max - val_min)


def denormalize(col, col_min, col_max):
    return col_min + col * (col_max - col_min)


# Split data into train and test datasets:
def split_data(data, test_size=0.2):
    # Shuffle the whole dataset (that's what frac=1 stands for):
    randomized_data = data.sample(frac=1)

    # Split data:
    border = int(test_size * len(data))
    test_set  = randomized_data[:border]
    train_set = randomized_data[border:]

    return train_set, test_set