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
