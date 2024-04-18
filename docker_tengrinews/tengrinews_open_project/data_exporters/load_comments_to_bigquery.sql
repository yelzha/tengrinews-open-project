-- Creating a table if it does not exist with the specified schema
CREATE TABLE IF NOT EXISTS `de-zoomcamp-412720.tengrinews_dataset.news_comments` (
    id INT64,
    date TIMESTAMP,
    object_id INT64,
    name STRING,
    text STRING,
    parent_id INT64,
    ip_country STRING,
    from_mobile INT64,
    rating INT64,
    user_id INT64
);

-- Merging data from a source (assumed to be a dataframe or similar structure) into the target table
MERGE `de-zoomcamp-412720.tengrinews_dataset.news_comments` AS target
USING (SELECT 
          id,
          TIMESTAMP(date) AS date,  -- Convert the 'date' column from DATETIME to TIMESTAMP
          object_id,
          name,
          text,
          parent_id,
          ip_country,
          from_mobile,
          rating,
          user_id
       FROM {{ df_1 }}) AS source  -- Ensure 'date' is the column name with datetime data in df_1
ON target.id = source.id
WHEN MATCHED THEN
  UPDATE SET
    target.date = source.date,
    target.object_id = source.object_id,
    target.name = source.name,
    target.text = source.text,
    target.parent_id = source.parent_id,
    target.ip_country = source.ip_country,
    target.from_mobile = source.from_mobile,
    target.rating = source.rating,
    target.user_id = source.user_id
WHEN NOT MATCHED THEN
  INSERT (id, date, object_id, name, text, parent_id, ip_country, from_mobile, rating, user_id)
  VALUES (source.id, source.date, source.object_id, source.name, source.text, source.parent_id, source.ip_country, source.from_mobile, source.rating, source.user_id);
