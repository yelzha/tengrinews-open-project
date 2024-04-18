-- models/staging/stg_news_comments.sql

WITH base AS (
    SELECT
        id,
        date,
        object_id,
        name,
        text,
        parent_id,
        ip_country,
        from_mobile,
        rating,
        user_id
    FROM `de-zoomcamp-412720.tengrinews_dataset.news_comments`
),

cleaned AS (
    SELECT
        id,
        TIMESTAMP_TRUNC(date, HOUR) AS hour,
        object_id,
        TRIM(name) AS name,
        TRIM(text) AS text,
        parent_id,
        ip_country,
        from_mobile,
        rating,
        user_id
    FROM base
    WHERE text IS NOT NULL
)

SELECT *
FROM cleaned