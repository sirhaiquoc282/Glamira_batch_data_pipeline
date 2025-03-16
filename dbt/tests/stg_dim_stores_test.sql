SELECT
    store_key,
    store_name
FROM
    {{ref("stg_dim_stores")}}
WHERE store_name IS NULL OR store_name = "" OR store_key < -1