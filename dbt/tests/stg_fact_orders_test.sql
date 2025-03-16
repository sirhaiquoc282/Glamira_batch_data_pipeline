SELECT
    order_line_key,
    order_key,
    store_key,
    order_date_key,
    product_key,
    stone_key,
    alloy_key,
    location_key,
    order_quantity,
    unit_price,
    line_total
FROM
    {{ref("stg_fact_orders")}}
WHERE 
    order_key < 0 OR 
    store_key < -1 OR
    order_date_key < 0 OR
    product_key IS NULL OR 
    stone_key IS NULL OR 
    alloy_key IS NULL OR 
    location_key IS NULL OR 
    order_quantity <= 0 OR
    unit_price < 0 OR 
    line_total < 0