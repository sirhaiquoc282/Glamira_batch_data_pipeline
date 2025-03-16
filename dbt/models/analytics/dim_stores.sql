SELECT
    store_key,
    store_name
FROM
    {{ref("stg_dim_stores")}}