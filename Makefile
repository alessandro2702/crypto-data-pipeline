# Define o caminho para o arquivo de configuração
CONFIG_FILE=crypto_pipeline/src/config.yaml

# Regra padrão
all: run

# Regra para rodar o Docker Compose
run:
	@MINIO_ACCESS_KEY=$$(grep 'minio_access_key:' $(CONFIG_FILE) | sed 's/.*: //') && \
	MINIO_SECRET_KEY=$$(grep 'minio_secret_key:' $(CONFIG_FILE) | sed 's/.*: //') && \
	MINIO_ROOT_USER=$$(grep 'minio_root_user:' $(CONFIG_FILE) | sed 's/.*: //') && \
	MINIO_ROOT_PASSWORD=$$(grep 'minio_root_password:' $(CONFIG_FILE) | sed 's/.*: //') && \
	echo "MINIO_ACCESS_KEY: $$MINIO_ACCESS_KEY" && \
	echo "MINIO_SECRET_KEY: $$MINIO_SECRET_KEY" && \
	echo "MINIO_ROOT_USER: $$MINIO_ROOT_USER" && \
	echo "MINIO_ROOT_PASSWORD: $$MINIO_ROOT_PASSWORD" && \
	MINIO_ACCESS_KEY=$$MINIO_ACCESS_KEY MINIO_SECRET_KEY=$$MINIO_SECRET_KEY \
	MINIO_ROOT_USER=$$MINIO_ROOT_USER MINIO_ROOT_PASSWORD=$$MINIO_ROOT_PASSWORD \
	docker compose up --build

.PHONY: all run
