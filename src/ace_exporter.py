from flask import Flask, Response
from api_client import APIClient
from metrics import MetricsHandler
import threading
import time

app = Flask(__name__)
api_client = APIClient('http://localhost:4414')
uri_server = "/apiv2/servers"
metrics_handler = MetricsHandler()

def process_server(server_data):
    server_details = api_client.fetch_uri(server_data['uri'])
    if server_details:
        app_count = process_applications(server_details)
        api_count = process_rest_apis(server_details)
        metrics_handler.update_metrics(server_data['name'], app_count, api_count)

def process_applications(server_details):
    applications_uri = server_details['children']['applications']['uri']
    applications_data = api_client.fetch_uri(applications_uri)
    if applications_data:
        return len(applications_data.get('children', []))
    return 0

def process_rest_apis(server_details):
    rest_apis_uri = server_details['children']['restApis']['uri']
    rest_apis_data = api_client.fetch_uri(rest_apis_uri)
    if rest_apis_data:
        return len(rest_apis_data.get('children', []))
    return 0

def update_metrics():
    while True:
        servers_data = api_client.fetch_uri(uri_server)
        if servers_data:
            for server in servers_data.get('children', []):
                process_server(server)
        time.sleep(60)  # Mise à jour toutes les 60 secondes

@app.route('/metrics')
def metrics():
    return Response(metrics_handler.get_metrics(), mimetype='text/plain')

if __name__ == '__main__':
    metrics_thread = threading.Thread(target=update_metrics)
    metrics_thread.start()
    app.run(host='0.0.0.0', port=8000)
