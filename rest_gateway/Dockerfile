FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./rest_gateway/

RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./rest_gateway/proto/*.proto

CMD ["python", "-m", "rest_gateway"]
