# Problem Statement for Tengrinews.kz Open Project

**Background:**
Tengrinews.kz, founded by Batyr Kazybayev and managed by LLC "Effective Media Liaison", is a prominent daily online news outlet in Kazakhstan. With a commitment to providing continuous, real-time news coverage, Tengrinews.kz has established itself as a critical source of information, reaching a wide audience through its digital platform.

**Objective:**
The goal of this project is to develop a robust data engineering pipeline to extract, transform, and load data from Tengrinews.kz efficiently. Specifically, the pipeline will focus on retrieving articles published the previous day and comments posted between the current date and the previous seven days. This data will be utilized to perform various business logic operations, which will aid in deeper data analysis and insights.

**Challenges:**
1. **Data Volume and Velocity:** The data is generated daily and continuously, which requires an efficient system for timely data scraping without overloading the website's servers or violating any usage policies.
2. **Data Quality and Consistency:** Ensuring the data scraped is accurate and consistent, given the dynamic nature of news content and user-generated comments.
3. **Complexity of Data Transformation:** Implementing advanced business logic that can handle diverse datasets and perform complex transformations for meaningful analysis.

**Proposed Solution:**
Develop a scalable data engineering solution that utilizes sophisticated scraping techniques with a paginator to fetch yesterday's articles. The solution will also implement a robust system to gather comments from the past week. These processes will be automated and scheduled to run at optimal times to ensure fresh data availability for daily analysis. The pipeline will also include components for error handling, data validation, and preprocessing to maintain high data quality and reliability.

**Impact:**
The successful implementation of this project will provide Tengrinews.kz with a powerful tool to monitor its outreach, understand reader engagement, and enhance its content strategy based on analytical insights. Moreover, it will serve as a scalable model that can be adapted for similar data-intensive environments requiring real-time data processing and analysis.


# Solution 
This project automates the extraction, transformation, and loading of data from Tengrinews.kz to facilitate detailed analytical processes. The primary goals include performing sentiment analysis and aggregating data based on geographic and temporal criteria to derive insightful information.

 ## Technology Used 
 - Python was used as a programming language. 
 - Terraform was used for managing infrastructure as code. 
 - Mage was used as an orchestrator. 
 - Google Cloud Storage was used as a data lake. 
 - DBT was used as a business transformer tool. 
 - Big Query was used as a data warehouse. 
 - Google Data Studio / Looker Studio was used for visualisation.


 ## Dashboard 
  ![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/c04551ea-16d6-4df3-9ff6-2092b41581eb)
  Dashboard Link: [https://lookerstudio.google.com/reporting/1347fff4-3c12-4cf9-a193-1c80e29b810f](https://lookerstudio.google.com/reporting/c93b1e3b-f273-4b93-b9cb-9878bc8b9cab)


# How to replicate solution? 
 ## Pre-requisites
 - Docker must be installed
 - Terraform must be installed
 - Mage must be installed 
 - DBT Cloud must be used 
 - Google Cloud account must be active


  ## Set Up Google Resources
  -	Create a project in Google Cloud
  -	Set up a service account. The service account needs to have the following roles:
    * BigQuery Admin
    * Compute Admin
    * Storage Admin     
  -	Create a key for the service account and download the json version 
  -	Change directory into the Terraform folder and edit the files to point to your key file
  -	Run the following command to create the GCP resources:
    ```bash
        terraform init
        terraform plan 
        terraform apply
     ```


 ## Mage Application Steps
 -	Clone the solution from GitHub 
 -	Change directory into to the solution folder 
 -	Run docker compose up to get Mage up and running
       ```bash
        docker compose up -d
     ```


 ## DBT Application Steps
 -	Clone the solution from GitHub 
 -	Change directory into to the "dbt" folder
 -	Go to the DBT cloud adn create new project based on code

       


# REPORT AND DOCUMENTATION
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
Implement advanced country to provide deeper insights into how news sentiment and topics vary across different regions. This feature will allow the identification of geographic patterns in news engagement and sentiment, aiding targeted content delivery and marketing strategies.
![image](https://github.com/yelzha/tengrinews-open-project/assets/54392243/0ac62dcc-402e-4aee-9cf4-833134e1105f)

Conclusion
The documentation outlines the complete workflow of the project and introduces an advanced feature to enhance geographic analytical capabilities. This additional geospatial analysis feature could significantly boost the project's ability to provide nuanced insights, supporting more strategic decision-making based on regional trends and patterns.


