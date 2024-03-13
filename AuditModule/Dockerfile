FROM python:3.12.1

RUN mkdir -p ./AuditModule
WORKDIR ./AuditModule

COPY . .

RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install protobuf
RUN pip install requests

CMD ["python", "main.py"]
