FROM python:3.12.1-slim-bullseye

RUN mkdir -p ./AuditModule
WORKDIR ./AuditModule

COPY . .

RUN pip install grpcio grpcio-tools protobuf requests

CMD ["python", "main.py"]
