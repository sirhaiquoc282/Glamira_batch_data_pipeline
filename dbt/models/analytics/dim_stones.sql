SELECT
    stone_key,
    stone_name
FROM
    {{ref("stg_dim_stones")}}
