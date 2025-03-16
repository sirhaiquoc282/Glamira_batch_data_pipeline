SELECT DISTINCT
    metal_key AS metal_key,
    CASE
        WHEN metal_key = 375 THEN '9k Gold'
        WHEN metal_key = 585 THEN '14k Gold'
        WHEN metal_key = 750 THEN '18k Gold'
        WHEN metal_key = 925 THEN "Silver"
        WHEN metal_key = 950 AND TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'[A-Za-zÀ-ÖØ-öø-ÿ\s-]+'), ' '))= 'Platin' THEN 'Platinum'
        WHEN metal_key = 950 AND TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'[A-Za-zÀ-ÖØ-öø-ÿ\s-]+'), ' '))= 'Palladium' THEN 'Palladium'
        ELSE "unknown"
    END AS metal_name
FROM {{ ref("stg_dim_alloys") }}
