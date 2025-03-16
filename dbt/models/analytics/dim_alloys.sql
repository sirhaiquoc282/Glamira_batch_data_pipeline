SELECT
    alloy_key,
    alloy_name,
    color_key,
    metal_key
FROM
    {{ref("stg_dim_alloys")}}