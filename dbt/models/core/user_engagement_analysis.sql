-- models/user_engagement_analysis.sql

WITH comment_details AS (
    SELECT
        object_id AS page_id,
        user_id,
        COUNT(id) AS comments_count,
        AVG(rating) AS avg_user_rating,
        COUNT(DISTINCT parent_id) AS reply_count
    FROM {{ ref('stg_news_comments') }}
    WHERE user_id IS NOT NULL
    GROUP BY object_id, user_id
)

SELECT
    d.page_id,
    d.page_url,
    d.title,
    d.category,
    COUNT(distinct c.user_id) AS unique_commenters,
    AVG(c.comments_count) AS avg_comments_per_user,
    SUM(c.reply_count) AS total_replies,
    AVG(c.avg_user_rating) AS avg_rating_on_page
FROM {{ ref('stg_news_data') }} d
JOIN comment_details c ON d.page_id = c.page_id
GROUP BY d.page_id, d.page_url, d.title, d.category
ORDER BY unique_commenters DESC, total_replies DESC
