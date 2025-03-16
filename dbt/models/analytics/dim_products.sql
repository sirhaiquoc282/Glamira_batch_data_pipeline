SELECT
    product_key,
    product_name
FROM
    {{ref("stg_dim_products")}}