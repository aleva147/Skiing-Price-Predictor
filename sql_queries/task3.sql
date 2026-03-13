USE filtered_offers_db;

-- -- a) Show 10 places with most offers:
SELECT place, COUNT(*) AS num_of_offers
FROM offers
GROUP BY place
ORDER BY COUNT(*) DESC
LIMIT 10;

-- -- b) Count how many offers there are for each place:
SELECT place, COUNT(*) AS num_of_offers 
FROM offers
GROUP BY place
ORDER BY num_of_offers DESC;

-- -- c) Count how many offers there are for each number of hotel stars (display the percentage as well):
SELECT stars, 
	   COUNT(*) AS num_of_offers, 
       ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM offers), 1) AS percentage
FROM offers
GROUP BY stars
ORDER BY stars;

-- -- d) Count how many offers there are for each price range (display the percentage as well):
WITH NumericOffers AS (
    SELECT CAST(REPLACE(price, '€', '') AS SIGNED) AS price_num
    FROM offers
),
PriceCategories AS (
    SELECT CASE
			WHEN price_num <= 500 THEN '500'
            WHEN price_num BETWEEN 501 AND 1500 THEN '501-1500'
            WHEN price_num BETWEEN 1501 AND 3000 THEN '1501-3000'
            ELSE '3000 or more' 
		   END AS category
    FROM NumericOffers
),
Counts AS (
    SELECT category, COUNT(*) AS count
    FROM PriceCategories
    GROUP BY category
),
TotalOffers AS (
    SELECT COUNT(*) AS total FROM offers
)
SELECT c.category, c.count, ROUND((c.count * 100.0) / t.total, 1) AS percentage
FROM Counts c, TotalOffers t
ORDER BY category;

-- -- e) Count how many offers there are for each service type (display the percentage as well):
SELECT service_type, 
	   COUNT(*) AS num_of_offers, 
       ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM offers), 1) AS percentage
FROM offers
GROUP BY service_type
ORDER BY service_type;
