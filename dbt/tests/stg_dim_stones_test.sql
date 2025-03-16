SELECT
    stone_key,
    stone_name
FROM
    {{ref("stg_dim_stones")}}
WHERE stone_name IS NULL OR stone_name = ""