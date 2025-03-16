WITH date_series AS (
    SELECT 
        DATE_ADD(DATE('2000-01-01'), INTERVAL n DAY) AS date_value
    FROM UNNEST(GENERATE_ARRAY(0, 36524, 1)) AS n
),

date_cte AS (
    SELECT 
        CAST(FORMAT_DATE('%Y%m%d', date_value) AS INT) AS date_key, 
        date_value AS date,
        FORMAT_DATE('%m-%d-%Y', date_value) AS full_date, -- MM-dd-yyyy
        CAST(FORMAT_DATE('%d', date_value) AS STRING) AS day_of_month,
        CASE 
            WHEN FORMAT_DATE('%d', date_value) IN ('01', '21', '31') THEN FORMAT_DATE('%d', date_value) || 'st'
            WHEN FORMAT_DATE('%d', date_value) IN ('02', '22') THEN FORMAT_DATE('%d', date_value) || 'nd'
            WHEN FORMAT_DATE('%d', date_value) IN ('03', '23') THEN FORMAT_DATE('%d', date_value) || 'rd'
            ELSE FORMAT_DATE('%d', date_value) || 'th'
        END AS day_suffix,
        FORMAT_DATE('%A', date_value) AS day_name,
        CAST(FORMAT_DATE('%w', date_value) AS INT) + 1 AS day_of_week,
        FORMAT_DATE('%W', date_value) AS week_of_month, 
        FORMAT_DATE('%Y-%m', date_value) AS month_year,
        FORMAT_DATE('%m', date_value) AS month,
        FORMAT_DATE('%B', date_value) AS month_name,
        FORMAT_DATE('%Q', date_value) AS quarter,
        CASE FORMAT_DATE('%Q', date_value)
            WHEN '1' THEN 'First'
            WHEN '2' THEN 'Second'
            WHEN '3' THEN 'Third'
            WHEN '4' THEN 'Fourth'
        END AS quarter_name,
        FORMAT_DATE('%Y', date_value) AS year,
        CONCAT('CY ', FORMAT_DATE('%Y', date_value)) AS year_name,
        FORMAT_DATE('%m%Y', date_value) AS MMYYYY,
        DATE_TRUNC(date_value, MONTH) AS first_day_of_month,
        DATE_ADD(DATE_TRUNC(date_value, MONTH), INTERVAL 1 MONTH) - 1 AS last_day_of_month,
        DATE_TRUNC(date_value, QUARTER) AS first_day_of_quarter,
        DATE_ADD(DATE_TRUNC(date_value, QUARTER), INTERVAL 3 MONTH) - 1 AS last_day_of_quarter,
        DATE_TRUNC(date_value, YEAR) AS first_day_of_year,
        DATE_ADD(DATE_TRUNC(date_value, YEAR), INTERVAL 1 YEAR) - 1 AS last_day_of_year,
        CASE 
            WHEN FORMAT_DATE('%A', date_value) IN ('Saturday', 'Sunday') THEN 0 
            ELSE 1 
        END AS is_week_day
    FROM date_series
)

SELECT * FROM date_cte
