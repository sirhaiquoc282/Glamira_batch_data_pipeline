SELECT DISTINCT
    FARM_FINGERPRINT(TRIM(option.value_label)) AS stone_key,
    TRIM(option.value_label) AS stone_name
FROM 
    {{ source('raw_glamira', 'summary') }},
    UNNEST(cart_products) AS product,
    UNNEST(product.option) AS option 
WHERE 
    option.option_label = 'diamond'
UNION ALL
SELECT
    -1 AS stone_key,
    "unknown" AS stone_name

