- models/core/engagement_analysis_by_news_page.sql

WITH page_comments AS (
    SELECT
        c.object_id AS page_id,
        COUNT(c.id) AS total_comments,
        AVG(c.rating) AS avg_rating,
        MAX(c.rating) AS max_rating,
        MIN(c.rating) AS min_rating
    FROM {{ ref('stg_news_comments') }} c
    GROUP BY c.object_id
),

page_views AS (
    SELECT
        p.page_id,
        p.page_url,
        p.title,
        p.category,
        p.content,
        p.views_count
    FROM {{ ref('stg_news_data') }} p
)

SELECT
    v.page_id,
    v.page_url,
    v.title,
    v.category,
    v.content,
    v.views_count,
    COALESCE(c.total_comments, 0) AS total_comments,
    COALESCE(c.avg_rating, 0) AS avg_rating,
    COALESCE(c.max_rating, 0) AS max_rating,
    COALESCE(c.min_rating, 0) AS min_rating,
    CASE
        WHEN v.views_count = 0 THEN 0
        ELSE c.total_comments / NULLIF(v.views_count, 0)
    END AS comments_per_view
FROM page_views v
LEFT JOIN page_comments c ON v.page_id = c.page_id
ORDER BY v.views_count DESC, c.total_comments DESC