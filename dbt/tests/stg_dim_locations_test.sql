SELECT
    location_key,
    city_name,
    region_name,
    country_short_name,
    country_long_name
FROM
    {{ref("stg_dim_locations")}}
WHERE 
    (city_name IS NULL OR city_name = "") OR
    (region_name IS NULL OR region_name = "") OR
    (country_short_name IS NULL OR country_short_name = "" )OR
    (country_long_name IS NULL OR country_long_name = "")