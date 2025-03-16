SELECT
    metal_key,
    metal_name
FROM
    {{ref("stg_dim_metals")}}
WHERE
    metal_name IS NULL OR metal_name = ""