FROM python:3.12.1

RUN mkdir -p ./api_getway
WORKDIR ./api_getway

COPY . .

RUN pip install flask
RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install protobuf

CMD ["python", "app.py"]
