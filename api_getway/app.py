import os

from flask import Flask, request, jsonify, render_template
from prometheus_client import generate_latest, Counter, Summary, Histogram, start_http_server
import grpc
import audit_service_pb2 as pb2
import audit_service_pb2_grpc as pb2_grpc
import requests
import uuid
import json
import time

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    _uuid = str(uuid.uuid1())
    error_status_request(_uuid, "Not found", 404, None)
    return render_template('404.html'), 404

REQUEST_TIME = Summary('request_processing_time', 'Time spent processing')
REQUEST_LATENCY = Histogram('request_latency_second', 'Request latency in seconds', ['method', 'endpoint'])
REQUEST_COUNTER = Counter('request_total', 'Total count of requests', ['method', 'endpoint', 'http_status'])

config_file_path = 'config/config.json'
with open(config_file_path, 'r') as config_file:
    conf = json.load(config_file)

channel = grpc.insecure_channel(f'{conf["gRPC_HOST"]}:{conf["gRPC_PORT"]}')
stub = pb2_grpc.MyServiceStub(channel)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        _uuid = str(uuid.uuid1())
        name = request.form.get('name')
        description = request.form.get('description')
        mode = request.form.get('mode')
        success = request.form.get('success')

        params = []
        for i in range(len(request.form.getlist("par_name"))):
            par_name = request.form.getlist("par_name")[i]
            par_description = request.form.getlist("par_description")[i]
            params.append({"name": par_name, "description": par_description})

        data = pb2.AuditRequest(
            uuid=_uuid,
            name=name,
            description=description,
            mode=mode,
            success=success
        )

        print(data)

        for param in params:
            param_msg = pb2.Param(name=param["name"], description=param["description"])
            data.params.append(param_msg)
        try:
            response = stub.CreateAudit(data)
        except grpc.RpcError as e:
            print(e)
            error_status_request(_uuid, e.details(), 500, e.args)
            return internal_server_error(500)
        with open('files/audit.json', 'r') as f:
            data = json.load(f)

        new_data = {"statusResponse": response.statusResponse, "id": response.uuid}
        data.append(new_data)

        with open('files/audit.json', 'w') as file:
            json.dump(data, file, indent=4)
    return render_template('home.html')


@app.route('/audit', methods=['GET'])
def return_json():
    if request.method == 'GET':
        with open('files/audit.json', 'r') as file:
            file_data = json.load(file)
    return jsonify(file_data)


def record_request_data(method, status_code, endpoint, start_time):
    REQUEST_COUNTER.labels(method=method, http_status=status_code, endpoint=endpoint).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_TIME.observe(request_latency)
    record_request_data(method=request.method, endpoint=request.path, status_code=response.status_code,
                        start_time=request.start_time)
    return response


def internal_server_error(error):
    return render_template('500.html'), error


def start_metrics_server(port=50000):
    start_http_server(port)
    print(f'Сервер метрик запущен на порту: {port}')


@app.route('/metrics')
def prom_metrics():
    return generate_latest()


def error_status_request(UUID, massage, status_code, http_error):
    url = f"{conf['loging_url']}"
    ip = request.headers.get('Host')
    hostname = os.getenv("hostname")
    project = os.getenv("PROJECT")
    if hostname == '' and project == '':
        hostname = "none_hostname"
        project = "none_project"
        return hostname, project

    data = {"massage": str(massage), "LogLevel": status_code, "levelStr": http_error, "ip": ip, "podName": hostname,
            "project": project, "UUID": UUID}
    try:
        requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    app.debug = True
    app.run(host=conf['api_host'], port=conf['api_port'])
