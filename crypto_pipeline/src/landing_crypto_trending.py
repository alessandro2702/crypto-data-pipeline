import json
import logging
from datetime import datetime
from io import BytesIO

from crypto_data_ingestion import CoinGeckoAPIClient, LocalStorage
from performance_report import profile

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_environment():
    # Create an instance of LocalStorage and save data to MinIO
    storage = LocalStorage()
    logger.info('Creating/Checking existence of Bucket in MinIO...')
    storage.create_bucket('crypto-data')

    return storage


@profile(script_name='landing_crypto_trending')
def main():

    # Check if the bucket already exists in MinIO, if not, create a new one.
    storage = prepare_environment()

    # Get the current date and configure directories and file names
    current_date = datetime.now().strftime('%Y-%m-%d')
    storage_directory = datetime.now().strftime(
        '10_landing/trending/%Y/%m/%d/'
    )
    file_name = f'trending_coins_{current_date}.json'
    object_dir_name = f'{storage_directory}{file_name}'

    # Instantiate the CoinGecko API client and get raw data
    coingecko = CoinGeckoAPIClient()
    logger.info('Fetching data from CoinGecko API...')
    raw_data = coingecko.get_data(
        '/coins/markets',
        params={
            'vs_currency': 'usd',
            'order': 'volume_desc',
            'per_page': 250,
            'page': 1,
        },
    )
    logger.info('Data fetched successfully.')
    logger.debug(f'Raw data: {raw_data}')

    # Convert raw data to bytes
    raw_data_bytes = BytesIO(json.dumps(raw_data).encode('utf-8'))

    logger.info('Saving raw data to MinIO container...')
    storage.save_raw_data(
        bucket_name='crypto-data',
        object_name=object_dir_name,
        data=raw_data_bytes,
        length=raw_data_bytes.getbuffer().nbytes,
        content_type='application/json',
    )
    logger.info('Data saved successfully.')


if __name__ == '__main__':
    main()
