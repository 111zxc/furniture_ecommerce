FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./grpc_user/

RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./grpc_user/proto/*.proto

CMD ["sh", "-c", "until nc -z ${POSTGRES_URL} 5432; do echo waiting for postgres; sleep 2; done; python -m grpc_user"]
