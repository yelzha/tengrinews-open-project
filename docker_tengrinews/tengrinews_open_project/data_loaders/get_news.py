import io
import pandas as pd
import datetime
import requests
from tengrinews_open_project.utils.tengrinews_data_loader import get_list_news
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    ingestion_date = kwargs['execution_date'] - datetime.timedelta(days=1)
    if kwargs['ingestion_date'] != '':
        ingestion_date = datetime.datetime.strptime(kwargs['ingestion_date'], '%Y-%m-%d')

    data = get_list_news(ingestion_date)

    return pd.DataFrame(data)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
