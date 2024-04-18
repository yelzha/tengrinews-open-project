import pyarrow as pa
import pyarrow.parquet as pq 
import os
from google.cloud import storage

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter



@data_exporter
def export_data(data, *args, **kwargs):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/.google/credentials/google_credentials.json'

    bucket_name = 'tengrinews-data-bucket'
    project_id = 'de-zoomcamp-412720'
    table_name = 'news_data.parquet'

    root_path = f'{bucket_name}/{table_name}'

    table = pa.Table.from_pandas(data)

    # Initialize GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    
    gcs = pa.fs.GcsFileSystem()

    for date in data['date'].unique():
        partition_path = f'{table_name}/date={date}'

        # Check if the partition already exists and delete it
        blobs = list(client.list_blobs(bucket, prefix=partition_path))
        if blobs:  # If list is not empty, blobs exist under the prefix
            for blob in blobs:
                blob.delete()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['date'],
        filesystem=gcs
    )