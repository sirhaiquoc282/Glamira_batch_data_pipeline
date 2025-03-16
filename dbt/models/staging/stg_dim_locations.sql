SELECT DISTINCT
    FARM_FINGERPRINT(
        CONCAT(
            COALESCE(NULLIF(NULLIF(TRIM(city), '-'), ''), 'unknown'),
            COALESCE(NULLIF(NULLIF(TRIM(region), '-'), ''), 'unknown'),
            COALESCE(NULLIF(NULLIF(TRIM(country_short), '-'), ''), 'unknown'),
            COALESCE(NULLIF(NULLIF(TRIM(country_long), '-'), ''), 'unknown')
        )
    ) AS location_key,
    COALESCE(NULLIF(NULLIF(TRIM(city), '-'), ''), 'unknown') AS city_name,
    COALESCE(NULLIF(NULLIF(TRIM(region), '-'), ''), 'unknown') AS region_name,
    COALESCE(NULLIF(NULLIF(TRIM(country_short), '-'), ''), 'unknown') AS country_short_name,
    COALESCE(NULLIF(NULLIF(TRIM(country_long), '-'), ''), 'unknown') AS country_long_name
FROM 
    {{source("raw_glamira", "locations")}}
WHERE NOT (
    (city = "" OR city = "-" OR city IS NULL) AND
    (region = "" OR region = "-" OR region IS NULL) AND
    (country_short = "" OR country_short = "-" OR country_short IS NULL) AND
    (country_long = "" OR country_long = "-" OR country_long IS NULL)
)
UNION ALL 

SELECT
    -1 AS location_key,
    "unknown" AS city_name,
    "unknown" AS region_name,
    "unknown" AS country_short_name,
    "unknown" AS country_long_name