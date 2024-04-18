This project automates the extraction, transformation, and loading of data from Tengrinews.kz to facilitate detailed analytical processes. The primary goals include performing sentiment analysis and aggregating data based on geographic and temporal criteria to derive insightful information.

System Architecture
Data Extraction:
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/baf43781-74eb-433f-8b01-0fe9c1128e91)

Source: Tengrinews.kz
Frequency: Daily scraping at 00:00 UTC
Tool: Custom Python script utilizing libraries like BeautifulSoup or Scrapy for web scraping.
Data Transformation and Storage:
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/a23a7b20-5868-4835-9f77-809d61d2befc)

``` python
import datetime


def parse_russian_date(date_str):
    if ':' not in date_str:
        date_str = f'{date_str} 00:00'
    # Russian month names mapping to their numeric values
    months = {
        'января': 1, 'февраля': 2, 'марта': 3,
        'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9,
        'октября': 10, 'ноября': 11, 'декабря': 12
    }
    
    # Current date
    today = datetime.datetime.now()
    
    # Handling relative dates
    if 'Сегодня' in date_str:
        date = today
        time_part = date_str.split()[1]
    elif 'Вчера' in date_str:
        date = today - datetime.timedelta(days=1)
        time_part = date_str.split()[1]
    else:
        # Splitting the date string by space
        day, month, year, time_part = date_str.split()
        day = int(day)
        year = int(year)
        month = months[month]
        date = datetime.datetime(year, month, day)
    
    # Parsing the time
    hour, minute = map(int, time_part.split(':'))
    
    # Combining date and time
    return datetime.datetime(date.year, date.month, date.day, hour, minute)

```

Processing: Python scripts are employed to clean and transform the scraped data.
Storage: The data is saved as a parquet file, partitioned by date, in a Google Cloud Storage (GCS) bucket to optimize query performance and manage costs effectively.
Data Enrichment:
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/9dd47f5c-3ee4-46ba-ae65-bcf2dc844c92)

``` python
import datetime


def parse_russian_date(date_str):
    if ':' not in date_str:
        date_str = f'{date_str} 00:00'
    # Russian month names mapping to their numeric values
    months = {
        'января': 1, 'февраля': 2, 'марта': 3,
        'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9,
        'октября': 10, 'ноября': 11, 'декабря': 12
    }
    
    # Current date
    today = datetime.datetime.now()
    
    # Handling relative dates
    if 'Сегодня' in date_str:
        date = today
        time_part = date_str.split()[1]
    elif 'Вчера' in date_str:
        date = today - datetime.timedelta(days=1)
        time_part = date_str.split()[1]
    else:
        # Splitting the date string by space
        day, month, year, time_part = date_str.split()
        day = int(day)
        year = int(year)
        month = months[month]
        date = datetime.datetime(year, month, day)
    
    # Parsing the time
    hour, minute = map(int, time_part.split(':'))
    
    # Combining date and time
    return datetime.datetime(date.year, date.month, date.day, hour, minute)

```


Comments Retrieval: Comments from the past 7 days are retrieved using an API to ensure that recent interactions are included.
Integration: News data and comments are integrated prior to loading into BigQuery.
Data Loading:

Database: Google BigQuery
Method: Batch loading of the processed and enriched data ensures efficiency and accuracy.
Data Analysis and Transformation:


``` python
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import datetime
from google.cloud import storage
import os
from tengrinews_open_project.utils.tengrinews_data_loader import get_comments



@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Load Parquet data from Google Cloud Storage within a specific date range.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Configuration and authentication
    # Example: Using an environment variable for Google credentials
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_credentials.json'

    # Setup client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/.google/credentials/google_credentials.json'

    client = storage.Client()
    table_name = 'news_data.parquet'
    bucket_name = 'tengrinews-data-bucket'
    bucket = client.bucket(bucket_name)

    # Calculate date range
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    # Generate the list of dates (assumes daily partitioning)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    
    # Generate list of date partitions
    date_partitions = pd.date_range(start=start_date, end=end_date).strftime('date=%Y-%m-%d').tolist()
    
    # Full path to GCS Parquet dataset
    frames = []
    for date_partition in date_partitions:
        url = f'gs://{bucket_name}/{table_name}/{date_partition}/'
        try:
            df = pd.read_parquet(url, engine='pyarrow')
            frames.append(df)
        except Exception as e:
            pass

    data = pd.concat(frames, ignore_index=True)

    comments = []

    for page_id in data['page_id']:
        list_comment = get_comments(page_id)
        comments += list_comment

    return pd.DataFrame(comments)



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


```

Tool: dbt (data build tool)
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/35be1f25-3681-4246-bf34-2956437eb6c7)

Transformations:
Sentiment analysis on news content and comments.
Data aggregation by country and other pertinent dimensions.
Additional Feature: Advanced Geospatial Analysis
Feature Description:
Implement advanced geospatial analysis to provide deeper insights into how news sentiment and topics vary across different regions. This feature will allow the identification of geographic patterns in news engagement and sentiment, aiding targeted content delivery and marketing strategies.
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/0ac62dcc-402e-4aee-9cf4-833134e1105f)

Implementation:

Geospatial Data Integration: Enhance the data model to include geographic information where possible (e.g., from user comments or IP addresses).
Analysis Tools: Utilize GIS (Geographic Information System) tools within BigQuery or integrate with external libraries in Python to perform spatial analysis.
Visualization: Extend existing visualizations in tools like Google Data Studio or Tableau to include maps and geographic heatmaps of data.
Conclusion
The documentation outlines the complete workflow of the project and introduces an advanced feature to enhance geographic analytical capabilities. This additional geospatial analysis feature could significantly boost the project's ability to provide nuanced insights, supporting more strategic decision-making based on regional trends and patterns.

![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/ad5e846a-6c49-4df9-a101-9d452833ac83)

