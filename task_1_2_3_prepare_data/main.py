from json_functions import *
from mysql_functions import *
from preprocessing_functions import *


# Define db and table names:
mysql_db_original     = 'original_offers_db'
mysql_db_filtered     = 'filtered_offers_db'
mysql_offers_table    = 'offers'
# Define paths:
scraped_data_original = 'scraped_data/original/'
scraped_data_filtered = 'scraped_data/filtered/offers.json'
data_from_db_original = 'data/offers_original.csv'
data_from_db_filtered = 'data/offers.csv'


# Merge all scraped offers into one JSON file and remove duplicates:
merge_json_files(scraped_data_original, scraped_data_filtered)
remove_duplicates(scraped_data_filtered)


# Create a mysql database and store scraped offers inside of a table:
create_db(mysql_db_original, mysql_offers_table)
store_data(scraped_data_filtered, mysql_db_original, mysql_offers_table)

# Load offers from the first database and store them in a CSV file:
retrieve_data(mysql_db_original, mysql_offers_table, data_from_db_original)


# Preprocess scraped data (fix invalid offers and remove outliers):
fix_invalid_offers(scraped_data_filtered)
remove_outliers(scraped_data_filtered)

# Create a second mysql database and store preprocessed offers inside of a table:
create_db(mysql_db_filtered, mysql_offers_table)
store_data(scraped_data_filtered, mysql_db_filtered, mysql_offers_table)

# Load offers from the second database and store them in a CSV file:
retrieve_data(mysql_db_filtered, mysql_offers_table, data_from_db_filtered)