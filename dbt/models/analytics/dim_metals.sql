SELECT
    metal_key,
    metal_name
FROM
    {{ref("stg_dim_metals")}}