SELECT
    location_key,
    city_name,
    region_name,
    country_short_name,
    country_long_name
FROM
    {{ref("stg_dim_locations")}}