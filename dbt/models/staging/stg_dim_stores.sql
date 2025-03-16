SELECT DISTINCT
    CAST(store_id AS INT) AS store_key,
    CONCAT('store-', store_id) AS store_name
FROM 
    {{ source('raw_glamira', 'summary') }} AS summary
WHERE store_id IS NOT NULL or store_id != ""
UNION ALL
SELECT 
    -1 AS store_id,
    "unknown" AS store_name
