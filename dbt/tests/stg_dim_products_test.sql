SELECT
    product_key,
    product_name
FROM
    {{ref("stg_dim_products")}}
WHERE 
    product_key < -1 OR product_name IS NULL OR product_name = ""