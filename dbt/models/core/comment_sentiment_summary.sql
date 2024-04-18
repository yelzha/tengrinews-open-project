-- models/comment_sentiment_summary.sql

WITH sentiment_summary AS (
    SELECT
        object_id AS page_id,
        AVG(rating) AS average_rating,
        COUNT(*) AS total_comments,
        COUNTIF(rating > 3) AS positive_comments,
        COUNTIF(rating <= 3) AS negative_comments
    FROM {{ ref('stg_news_comments') }}
    GROUP BY object_id
),

page_details AS (
    SELECT
        page_id,
        page_url,
        title,
        category
    FROM {{ ref('stg_news_data') }}
)

SELECT
    p.page_id,
    p.page_url,
    p.title,
    p.category,
    s.average_rating,
    s.total_comments,
    s.positive_comments,
    s.negative_comments,
    s.positive_comments / NULLIF(s.total_comments, 0) AS positivity_ratio
FROM page_details p
JOIN sentiment_summary s ON p.page_id = s.page_id
ORDER BY positivity_ratio DESC, average_rating DESC