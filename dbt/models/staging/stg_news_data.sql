-- models/staging/stg_news_data.sql

WITH base AS (
    SELECT
        page_url,
        category,
        page_id,
        title,
        content,
        hashtags,
        date,
        views_count,
        datetime
    FROM `de-zoomcamp-412720.tengrinews_dataset.news_data`
),

cleaned AS (
    SELECT
        page_url,
        LOWER(category) AS category,
        page_id,
        TRIM(title) AS title,
        TRIM(content) AS content,
        SPLIT(hashtags, ',') AS hashtags_array,
        date,
        views_count,
        TIMESTAMP_SECONDS(CAST(datetime / 1000000000 AS INT64)) AS timestamp
    FROM base
    WHERE page_id IS NOT NULL
)

SELECT *
FROM cleaned
