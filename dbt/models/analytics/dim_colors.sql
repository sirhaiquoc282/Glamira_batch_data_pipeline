SELECT
    color_key,
    color_name
FROM
    {{ref("stg_dim_colors")}}