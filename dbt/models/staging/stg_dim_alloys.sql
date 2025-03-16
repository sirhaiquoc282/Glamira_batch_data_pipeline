SELECT DISTINCT 
    FARM_FINGERPRINT(TRIM(alloy_name)) AS alloy_key,
    TRIM(alloy_name) AS alloy_name,
    FARM_FINGERPRINT(TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'[A-Za-zÀ-ÖØ-öø-ÿ\s-]+'), ' '))) AS color_key,
    COALESCE(
        CAST(NULLIF(TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'\d+'), ' ')), '') AS INT64), 
        -1
    ) AS metal_key
FROM 
    {{ source('raw_glamira', 'summary') }},
    UNNEST(cart_products) AS product, 
    UNNEST(product.option) AS option,
    UNNEST(SPLIT(option.value_label, '/')) AS alloy_name
WHERE 
    option.option_label = 'alloy'

UNION ALL

SELECT
    -1 AS alloy_key,
    'unknown' AS alloy_name,
    -1 AS color_key,
    -1 AS metal_key
