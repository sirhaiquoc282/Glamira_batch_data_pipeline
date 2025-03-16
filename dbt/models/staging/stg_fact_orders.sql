WITH order_diamond AS (
    SELECT DISTINCT
        CAST(time_stamp AS STRING) AS time_stamp,
        ip,
        CAST(store_id AS INT64) AS store_id,
        CAST(CAST(order_id AS NUMERIC) AS STRING) AS order_id,
        CAST(product.product_id AS STRING) AS product_id,
        SAFE_CAST(product.amount AS INT64) AS amount,
        SAFE_CAST(
            REPLACE(
                REGEXP_REPLACE(
                    CASE 
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = ',' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r'\.') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), '.', ''), ',', '.')
                        
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = '.' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r',') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), ',', ''), '.', ',')

                        ELSE COALESCE(NULLIF(product.price, ''), '0') 
                    END, 
                    r'[^\d,.]', ''
                ),
                ',', '.' 
            ) AS FLOAT64
        ) AS price,
        product.currency,
        TRIM(option.value_label) AS value_label
    FROM 
        {{source('raw_glamira', 'summary')}}, 
        UNNEST(cart_products) AS product,
        UNNEST(product.option) AS option
    WHERE 
        collection = 'checkout_success' 
        AND option.option_label = 'diamond'
), 
order_alloy AS (
    SELECT DISTINCT
        CAST(time_stamp AS STRING) AS time_stamp,
        ip,
        CAST(store_id AS INT64) AS store_id,
        CAST(CAST(order_id AS NUMERIC) AS STRING) AS order_id,
        CAST(product.product_id AS STRING) AS product_id,
        SAFE_CAST(product.amount AS INT64) AS amount,
        SAFE_CAST(
            REPLACE(
                REGEXP_REPLACE(
                    CASE 
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = ',' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r'\.') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), '.', ''), ',', '.')
                        
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = '.' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r',') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), ',', ''), '.', ',')

                        ELSE COALESCE(NULLIF(product.price, ''), '0') 
                    END, 
                    r'[^\d,.]', ''
                ),
                ',', '.' 
            ) AS FLOAT64
        ) AS price,
        product.currency,
        TRIM(option.value_label) AS value_label
    FROM 
        {{source('raw_glamira', 'summary')}}, 
        UNNEST(cart_products) AS product,
        UNNEST(product.option) AS option
    WHERE 
        collection = 'checkout_success' 
        AND option.option_label = 'alloy'
),
order_none_option AS (
    SELECT DISTINCT
        CAST(time_stamp AS STRING) AS time_stamp,
        ip,
        CAST(store_id AS INT64) AS store_id,
        CAST(CAST(order_id AS NUMERIC) AS STRING) AS order_id,
        CAST(product.product_id AS STRING) AS product_id, 
        "unknown" AS alloy_name,
        "unknown" AS stone_name,
        SAFE_CAST(product.amount AS NUMERIC) AS amount,
        SAFE_CAST(
            REPLACE(
                REGEXP_REPLACE(
                    CASE 
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = ',' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r'\.') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), '.', ''), ',', '.')
                        
                        WHEN SUBSTR(COALESCE(NULLIF(product.price, ''), '0'), LENGTH(COALESCE(NULLIF(product.price, ''), '0')) - 2, 1) = '.' 
                            AND REGEXP_CONTAINS(COALESCE(NULLIF(product.price, ''), '0'), r',') 
                        THEN REPLACE(REPLACE(COALESCE(NULLIF(product.price, ''), '0'), ',', ''), '.', ',')

                        ELSE COALESCE(NULLIF(product.price, ''), '0') 
                    END, 
                    r'[^\d,.]', ''
                ),
                ',', '.' 
            ) AS FLOAT64
        ) AS price,
        product.currency
    FROM 
        {{source('raw_glamira', 'summary')}}, 
        UNNEST(cart_products) AS product
    WHERE 
        collection = 'checkout_success' 
        AND (ARRAY_LENGTH(product.option) = 0)
),
processed_orders AS (
    SELECT DISTINCT
        COALESCE(od.time_stamp, oa.time_stamp) AS time_stamp,
        COALESCE(od.ip, oa.ip) AS ip,
        COALESCE(od.store_id, oa.store_id) AS store_id,
        COALESCE(od.order_id, oa.order_id) AS order_id,
        COALESCE(od.product_id, oa.product_id) AS product_id,
        CAST(TRIM(oa.value_label) AS STRING) AS alloy_name, 
        CAST(TRIM(od.value_label) AS STRING) AS stone_name,
        COALESCE(od.amount, oa.amount) AS amount,
        COALESCE(od.price, oa.price) AS price,
        COALESCE(od.currency, oa.currency) AS currency
    FROM 
        order_diamond od
    FULL OUTER JOIN order_alloy oa 
        ON od.time_stamp = oa.time_stamp
        AND od.order_id = oa.order_id
        AND od.product_id = oa.product_id
    UNION ALL
    SELECT * FROM order_none_option
)

SELECT
    FARM_FINGERPRINT(CONCAT(po.time_stamp, po.order_id, po.product_id)) AS order_line_key,
    SAFE_CAST(po.order_id AS NUMERIC) AS order_key,
    po.store_id AS store_key,
    SAFE_CAST(FORMAT_DATE('%Y%m%d', DATE(TIMESTAMP_SECONDS(SAFE_CAST(po.time_stamp AS INT64)))) AS INT64) AS order_date_key,
    SAFE_CAST(po.product_id AS NUMERIC) AS product_key,
    CASE 
        WHEN po.stone_name IS NULL OR TRIM(po.stone_name) = '' THEN -1
        ELSE FARM_FINGERPRINT(po.stone_name)
    END AS stone_key,
    FARM_FINGERPRINT(po.alloy_name) AS alloy_key,
    CASE 
        WHEN 
            COALESCE(NULLIF(NULLIF(TRIM(l.city), '-'), ''), 'unknown') = 'unknown' AND
            COALESCE(NULLIF(NULLIF(TRIM(l.region), '-'), ''), 'unknown') = 'unknown' AND
            COALESCE(NULLIF(NULLIF(TRIM(l.country_short), '-'), ''), 'unknown') = 'unknown' AND
            COALESCE(NULLIF(NULLIF(TRIM(l.country_long), '-'), ''), 'unknown') = 'unknown'
        THEN -1
        ELSE FARM_FINGERPRINT(
            CONCAT(
                COALESCE(NULLIF(NULLIF(TRIM(l.city), '-'), ''), 'unknown'),
                COALESCE(NULLIF(NULLIF(TRIM(l.region), '-'), ''), 'unknown'),
                COALESCE(NULLIF(NULLIF(TRIM(l.country_short), '-'), ''), 'unknown'),
                COALESCE(NULLIF(NULLIF(TRIM(l.country_long), '-'), ''), 'unknown')
            )
        )
    END AS location_key,
    SAFE_CAST(po.amount AS INT64) AS order_quantity,
    SAFE_CAST(po.price AS FLOAT64)*SAFE_CAST(er.exchange_rate AS FLOAT64) AS unit_price,
    COALESCE(
    SAFE_CAST(po.price AS FLOAT64), 0
) * COALESCE(
    SAFE_CAST(er.exchange_rate AS FLOAT64), 1
) * COALESCE(
    SAFE_CAST(po.amount AS INT64), 0
) AS line_total
FROM 
    processed_orders po
LEFT JOIN {{source("raw_glamira","locations")}} l 
    ON po.ip = l.ip
LEFT JOIN {{ref("exchange_rate")}} er 
    ON po.currency = er.symbol


