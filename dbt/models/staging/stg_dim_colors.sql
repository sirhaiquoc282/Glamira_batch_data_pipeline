SELECT DISTINCT
    FARM_FINGERPRINT(TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'[A-Za-zÀ-ÖØ-öø-ÿ\s-]+'), ' '))) as color_key,
    TRIM(ARRAY_TO_STRING(REGEXP_EXTRACT_ALL(alloy_name, r'[A-Za-zÀ-ÖØ-öø-ÿ\s-]+'), ' ')) AS color_name
FROM {{ref("stg_dim_alloys")}}
WHERE color_key != -1
UNION ALL
SELECT
    -1 AS color_key,
    "unknown" AS color_name