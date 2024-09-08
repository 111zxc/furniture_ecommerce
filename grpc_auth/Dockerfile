FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./grpc_auth/

RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./grpc_auth/proto/*.proto

CMD ["python", "-m", "grpc_auth"]