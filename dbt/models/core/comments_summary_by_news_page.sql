-- models/core/comments_summary_by_news_page.sql

WITH page_details AS (
    SELECT
        p.page_id,
        p.page_url,
        p.title,
        p.category,
        p.content,
        p.views_count,
        p.date AS published_date,
        COUNT(c.id) AS total_comments,
        AVG(c.rating) AS average_rating,
        COUNT(DISTINCT c.user_id) AS unique_users
    FROM {{ ref('stg_news_data') }} p
    LEFT JOIN {{ ref('stg_news_comments') }} c
        ON p.page_id = c.object_id
    GROUP BY p.page_id, p.page_url, p.title, p.category, p.content, p.views_count, p.date
),

comment_geo_distribution AS (
    SELECT
        object_id,
        ip_country,
        COUNT(*) AS comments_count
    FROM {{ ref('stg_news_comments') }}
    GROUP BY object_id, ip_country
)

SELECT
    d.page_id,
    d.page_url,
    d.title,
    d.category,
    d.content,
    d.views_count,
    d.published_date,
    d.total_comments,
    d.average_rating,
    d.unique_users,
    g.ip_country,
    g.comments_count
FROM page_details d
LEFT JOIN comment_geo_distribution g
    ON d.page_id = g.object_id
ORDER BY d.page_id, g.comments_count DESC