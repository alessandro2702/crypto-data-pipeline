# Cryptocurrency Data Pipeline

Este projeto é uma aplicação Python desenvolvida para facilitar a ingestão e o processamento de dados de sobre criptomoedas. O objetivo é fornecer uma solução robusta e escalável para coletar, armazenar e analisar dados transacionais de forma eficiente.

## Funcionalidades

- **Ingestão de Dados:** Coleta dos dados de transações realizadas através da API da CoinGecko.  
- **Armazenamento:** Salvamento dos dados em um formato estruturado e acessível, como CSV, JSON ou até mesmo no ambiente S3 self-hosted do MinIO.

## Requisitos

Para executar este projeto, você precisará dos seguintes componentes:

- **Python 3.11 ou superior**  
- **Docker**
- **Bibliotecas Python:**
  - `Poetry`
  - `Crypto-Data-Ingestion`

## Instalação

Será necessário instalar as dependências do pacote usando o comando:

```
poetry install
```

Após instalar as dependências, basta inicializar a execução do pipeline na raiz do projeto, através do comando Make:

```
make
```

No fim do processamento, você pode verificar os dados disponíveis dentro do container do MinIO criado pelo processo na URL:

```
http://127.0.0.1:9000
```

As credenciais DEFAULT do Storage é: 
  - LOGIN: crypto_admin
  - PASSWORD: crypto_password

Após a execução do pipeline, o processo irá gerar relatórios de performance dos scripts executados, apresentando informações úteis como: Uso de CPU, Uso de Memória e Tempo de Execução em Nanosegundos para avaliação da performance do pipeline.

Esses relatórios estão disponíveis no diretório home do usuário:

```
~/crypto_pipeline/reports/
```

