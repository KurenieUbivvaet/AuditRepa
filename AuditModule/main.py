import time
import json
import grpc
from concurrent import futures
import requests
from requests.exceptions import HTTPError
import audit_service_pb2 as pb2
import audit_service_pb2_grpc as pb2_grpc

class MyService(pb2_grpc.MyServiceServicer):
    data_conf_file_path = 'config/data_conf.json'
    with open(data_conf_file_path, 'r') as data_conf_file:
        data_conf = json.load(data_conf_file)

    def CreateAudit(self, request, context):
        uuid = request.uuid
        name = request.name
        description = request.description
        mode = request.mode
        success = request.success
        params = []
        for param in request.params:
            params.append({"name": param.name, "description": param.description})

        events = []
        events.append({"name": name, "description": description, "mode": mode, "success": success, "params": params})

        print(params)
        data = self.CreateJsonAudit(events=events)
        HttpRequest = self.RestRequest(self.data_conf["X-Node-ID"], data)
        return pb2.AuditResponse(uuid=uuid, statusResponse=str(HttpRequest))

    def CreateJsonAudit(self, events):
        TestJsonPath = f'files/AuditModul.json'
        main_data = {
            "metamodelVersion": f"{self.data_conf['metamodelVersion']}",
            "module": f"{self.data_conf['module']}",
        }
        main_data.update({"events": events})
        with open(TestJsonPath, 'w+') as test_json:
            json.dump(main_data, test_json, indent=4)
        return main_data

    def RestRequest(self, XNodeId, data):
        url = f'{server_conf["SERVER_HTTP"]}://{server_conf["SERVER_HOST"]}:{server_conf["SERVER_PORT"]}'
        headers = {'X-Node-Id': XNodeId}
        try:
            r = requests.post(url, headers=headers, data=data)
            status = r.status_code
        except requests.ConnectionError as e:
            print(e)
            status = "500"
        except requests.HTTPError as e:
            print(e)
            status = e.response.status_code
        return status

server_conf_file_path = 'config/server_conf.json'
with open(server_conf_file_path, 'r') as server_conf_file:
    server_conf = json.load(server_conf_file)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
server.add_insecure_port(f'{server_conf["gRPC_HOST"]}:{server_conf["gRPC_PORT"]}')
server.start()
print(f"сервер запущен {server_conf["gRPC_HOST"]}:{server_conf["gRPC_PORT"]}")

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)