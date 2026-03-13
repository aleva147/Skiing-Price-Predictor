USE filtered_offers_db;

-- -- List num of collected offers:
-- SELECT COUNT(*) FROM offers;

-- -- a) Count how many offers there are for each place:
SELECT place, COUNT(*) AS num_of_offers 
FROM offers
GROUP BY place
ORDER BY num_of_offers;

-- -- b) Count how many offers there are for hotels with 4 and 5 stars:
SELECT stars, COUNT(*) AS num_of_offers
FROM offers
GROUP BY stars
ORDER BY stars;

-- -- c) Count how many offers provide "all inclusive" service:
SELECT COUNT(*) AS num_of_all_inclusive_offers 
FROM offers
WHERE service_type = "all inclusive";

-- -- d) Count how many offers are for 12 or more nights:
SELECT COUNT(*) AS num_of_offers_with_12_or_more_nigths
FROM offers
WHERE num_of_nights >= 12;

-- -- e) Show top 30 most expensive offers:
SELECT *
FROM offers
ORDER BY CAST(REPLACE(price, '€', '') AS UNSIGNED) DESC
LIMIT 30;

-- -- f) Show top 30 most expensive offers that provide "all inclusive" service:
SELECT *
FROM offers
WHERE service_type = "all inclusive"
ORDER BY CAST(REPLACE(price, '€', '') AS UNSIGNED) DESC
LIMIT 30;
