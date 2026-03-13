import os
import json



# Fix invalid data in scraped offers:
def fix_invalid_offers(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_data = []
    cnt_invalid = 0
    cnt_removed = 0

    for obj in data:
        # Remove offers with incorrect field formats:
        if obj.get('place') == '' or obj.get('country') == '' or obj.get('hotel') == '' or obj.get('stars') == '':
            cnt_removed += 1
            continue
        if obj.get('room_size').split(' ')[1] != 'm2' or int(obj.get('room_size').split(' ')[0]) < 11:
            cnt_removed += 1
            continue

        # Offers without hotel stars are assigned 3 stars:
        if obj['stars'] < 1 or obj['stars'] > 5:
            cnt_invalid += 1
            obj['stars'] = 3
            

        filtered_data.append(obj)
    
    print(f"Removed {cnt_removed} offers that had incorrect data format.")
    print(f"Fixed {cnt_invalid} offers that had missing data.")

    # Save the filtered list
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)


# Remove outliers:
def remove_outliers(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_data = []

    for obj in data:
        # Extra expensive offers:
        price = int(obj.get('price')[:-1])
        if price >= 6000: continue
        if price <= 100: continue

        # Extra large rooms:
        price = int(obj.get('price')[:-1])
        room_size = int(obj.get('room_size')[:-3])
        if room_size > 70: continue
        if room_size <= 16 and price >= 3500: continue
        elif room_size > 16 and room_size <= 20 and price >= 4200: continue
        elif room_size >= 40 and price < 500: continue

        # Incredibly cheap long offers:
        if obj.get('num_of_nights') >= 15 and price < 700 or obj.get('num_of_nights') <= 4 and price >= 2500:
            continue

        # Star related outliers:
        if obj.get('stars') == 2 and price >= 4000 \
        or obj.get('stars') == 5 and price <= 800 \
        or obj.get('stars') == 4 and price <= 500 \
        or obj.get('stars') == 3 and (price <= 350 or price > 5500):
            continue

        # Remove offers for places that have very little offers:
        # if obj.get('place') in ['Courchevel', 'Les Houches-Chamonix', 'Superdevoluy', 'Malga Ciapela - Marmolada', 'Isola 2000', 'Montgenevre', 'Alagna Monterosa', 'Valfrejus', 'Auris En Oisans', 'Meribel']:
        #     continue 

        filtered_data.append(obj)

    print(f"Removed {len(data) - len(filtered_data)} outliers.")

    # Save the filtered list
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

