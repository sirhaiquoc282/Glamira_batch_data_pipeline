SELECT
    color_key,
    color_name
FROM {{ref("stg_dim_colors")}}
WHERE 
    (color_key IS NULL)
    OR
    (color_name IS NULL OR color_name = "")