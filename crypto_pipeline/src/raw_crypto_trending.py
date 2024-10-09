import logging
from datetime import datetime
from crypto_data_ingestion import LocalStorage, DataProcessing
from performance_report import profile_code

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@profile_code('raw_crypto_trending')
def main():
    # Instantiate storage and data processing classes
    logger.info('Instantiating storage and data processing classes.')
    storage = LocalStorage()
    engine = DataProcessing(storage)

    # Get the current date
    current_date = datetime.now().strftime('%Y/%m/%d')
    file_name = f'trending_coins_{datetime.now().strftime("%Y-%m-%d")}.json'
    logger.info(f'Current date: {current_date}, File name: {file_name}')

    # Read raw data from MinIO Bucket
    logger.info('Reading raw data from MinIO Bucket.')
    df = engine.read_raw_data(
        'json',
        'crypto-data',
        f'10_landing/trending/{current_date}/{file_name}',
    )

    # Infer and convert column data types
    logger.info('Converting column data types.')
    df = df.convert_dtypes()

    # Register DataFrame in DuckDB
    logger.info('Registering DataFrame in DuckDB.')
    engine.register_dataframe(df, 'trending_coins')

    # Execute an SQL query through the DuckDB engine
    logger.info('Executing SQL query through DuckDB engine.')
    query_result = engine.run_sql_query(
        'SELECT * FROM trending_coins WHERE market_cap > 1000000'
    )

    # Save the Delta table to MinIO
    logger.info('Saving the Delta table to MinIO.')
    engine.save_delta_table(
        table_path='s3a://crypto-data/20_raw/trending_coins',
        write_mode='overwrite',
        schema_mode='overwrite',
        data=query_result,
    )


if __name__ == '__main__':
    main()
