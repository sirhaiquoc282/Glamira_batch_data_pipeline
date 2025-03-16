SELECT DISTINCT
    p.product_id AS product_key,
    p.product_name
FROM {{ source('raw_glamira', 'products') }} p
WHERE p.product_id IS NOT NULL 
    AND p.product_name IS NOT NULL

UNION ALL

SELECT
    -1 AS product_key,
    "unknown" AS product_name
