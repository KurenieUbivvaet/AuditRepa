FROM python:3.12.1-slim-bullseye

RUN mkdir -p ./api_getway
WORKDIR ./api_getway

COPY . .

RUN pip install flask grpcio grpcio-tools protobuf

CMD ["python", "app.py"]
