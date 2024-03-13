from flask import Flask, request, jsonify, render_template
import grpc
import audit_service_pb2 as pb2
import audit_service_pb2_grpc as pb2_grpc
import uuid
import json

app = Flask(__name__)


config_file_path = 'config/config.json'
with open(config_file_path, 'r') as config_file:
    conf = json.load(config_file)

channel = grpc.insecure_channel(f'{conf["gRPC_HOST"]}:{conf["gRPC_PORT"]}')
stub = pb2_grpc.MyServiceStub(channel)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        UUID = str(uuid.uuid4())
        name = request.form.get('name')
        description = request.form.get('description')
        mode = request.form.get('mode')
        success = request.form.get('success')

        params = []
        for i in range(len(request.form.getlist("parName"))):
            parName = request.form.getlist("parName")[i]
            parDescription = request.form.getlist("parDescription")[i]
            params.append({"name": parName, "description": parDescription})

        data = pb2.AuditRequest(
            uuid=UUID,
            name=name,
            description=description,
            mode=mode,
            success=success
        )

        print(data)

        for param in params:
            param_msg = pb2.Param(name=param["name"], description=param["description"])
            data.params.append(param_msg)

        response = stub.CreateAudit(data)
        with open('files/audit.json', 'r') as f:
            data = json.load(f)

        new_data = {"statusResponse": response.statusResponse, "id": response.uuid}
        data.append(new_data)

        with open('files/audit.json', 'w') as file:
            json.dump(data, file, indent=4)
    return render_template('home.html')

@app.route('/audit', methods=['GET'])
def ReturnJson():
    if request.method == 'GET':
        with open('files/audit.json', 'r') as file:
            file_data = json.load(file)
    return jsonify(file_data)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
