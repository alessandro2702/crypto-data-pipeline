import json
import logging
from datetime import datetime
from io import BytesIO

from crypto_data_ingestion import CoinGeckoAPIClient, LocalStorage

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    # Obter a data atual
    data = datetime.now()
    data_atual = data.strftime('%Y-%m-%d')
    ano = data.strftime('%Y')
    mes = data.strftime('%m')
    dia = data.strftime('%d')

    # Diretório onde os dados serão armazenados
    storage_directory = f'10_landing/trending/{ano}/{mes}/{dia}/'
    file_name = f'trending_coins_{data_atual}.json'
    object_dir_name = f'{storage_directory}{file_name}'

    # Instanciando o cliente da API da CoinGecko
    coingecko = CoinGeckoAPIClient()

    # Obtendo os dados brutos
    logger.info('Obtendo dados da API CoinGecko...')
    raw_data = coingecko.get_data(
        '/coins/markets',
        params={
            'vs_currency': 'usd',
            'order': 'volume_desc',
            'per_page': 250,
            'page': 1,
        },
    )
    raw_data_bytes = BytesIO(json.dumps(raw_data).encode('utf-8'))

    logger.info('Dados obtidos com sucesso.')
    logger.debug(f'Dados brutos: {raw_data}')

    # Cria uma instância de LocalStorage
    storage = LocalStorage()

    logger.info('Criando bucket no MinIO...')
    storage.create_bucket('crypto-data')

    logger.info('Salvando dados brutos no container do MinIO...')
    storage.save_raw_data(
        bucket_name='crypto-data',
        object_name=object_dir_name,
        data=raw_data_bytes,
        length=len(raw_data_bytes.getvalue()),
        content_type='application/json',
    )
    logger.info('Dados salvos com sucesso.')


if __name__ == '__main__':
    main()
