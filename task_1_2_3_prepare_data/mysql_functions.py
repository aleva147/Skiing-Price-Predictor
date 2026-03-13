import mysql.connector
import os
import json
import csv



# Create a mysql database and a table for offers:
def create_db(db_name, table_name):
    # Connect to MySQL server:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root'
    )

    cursor = conn.cursor()

    # Drop the database if it already exists:
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

    # Create a database:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")

    # Create the offers table:
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        country VARCHAR(25),
        place VARCHAR(100),
        hotel VARCHAR(100),
        stars INT,
        month CHAR(3),
        date VARCHAR(11),
        num_of_nights INT,
        num_of_guests INT,
        service_type VARCHAR(30),
        room_size VARCHAR(10),
        price VARCHAR(10)
    )
    """
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


# Insert all scraped json data into the created database:
def store_data(json_file_path, db_name, table_name):
    file_path = os.path.join(os.getcwd(), json_file_path)

    # Connect to MySQL database:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database=db_name
    )

    cursor = conn.cursor()

    # Prepare the insert statement:
    insert_query = f"""
    INSERT INTO {table_name} (
        country, place, hotel, stars, month, date,
        num_of_nights, num_of_guests, service_type, room_size, price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each json object into the database:
    with open(file_path, 'r', encoding='utf-8') as f:
        offers = json.load(f)

    for offer in offers:
        data_tuple = (
            offer.get('country'),
            offer.get('place'),
            offer.get('hotel'),
            offer.get('stars'),
            offer.get('month'),
            offer.get('date'),
            offer.get('num_of_nights'),
            offer.get('num_of_guests'),
            offer.get('service_type'),
            offer.get('room_size'),
            offer.get('price')
        )
        cursor.execute(insert_query, data_tuple)

    # Commit the transaction and close the connection:
    conn.commit()
    cursor.close()
    conn.close()

 
# Collect data from the mysql table and store it in a csv file:
def retrieve_data(db_name, table_name, csv_file_path):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database=db_name
    )

    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)

    cursor.close()
    conn.close()
