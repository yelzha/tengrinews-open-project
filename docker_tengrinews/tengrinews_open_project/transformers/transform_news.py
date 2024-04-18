import pandas as pd
from tengrinews_open_project.utils.date_utils import parse_russian_date
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs) -> pd.DataFrame:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    data['page_id'] = data['page_id'].astype('int64')
    data['datetime'] = data['date_txt'].apply(parse_russian_date)
    data['date'] = data['datetime'].dt.date
    data['views_count'] = data['views_count'].astype('int64')

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


@test
def test_data_types(output) -> None:
    assert output['page_url'].dtype == 'object', 'The column is not of type object.'
    assert output['category'].dtype == 'object', 'The column is not of type object.'
    assert output['page_id'].dtype == 'int64', 'The column is not of type int64.'
    assert output['title'].dtype == 'object', 'The column is not of type object.'
    assert output['content'].dtype == 'object', 'The column is not of type object.'
    assert output['hashtags'].dtype == 'object', 'The column is not of type object.'
    assert output['datetime'].dtype == 'datetime64[ns]', 'The column is not of type datetime64[ns].'
    assert output['views_count'].dtype == 'int64', 'The column is not of type int64.'


@test
def test_views_count(output) -> None:
    assert all(output['views_count'] >= 0), 'The column is not of type int64.'
