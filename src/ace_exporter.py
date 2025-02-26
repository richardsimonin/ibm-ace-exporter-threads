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
        process_applications(server_details, server_data['name'])

def process_applications(server_details, server_name):
    applications_uri = server_details['children']['applications']['uri']
    applications_data = api_client.fetch_uri(applications_uri)
    if applications_data:
        for app in applications_data.get('children', []):
            app_details = api_client.fetch_uri(app['uri'])
            if app_details:
                process_message_flows(app_details, server_name, app['name'])

def process_message_flows(app_details, server_name, app_name):
    message_flows_uri = app_details['children']['messageFlows']['uri']
    message_flows_data = api_client.fetch_uri(message_flows_uri)
    if message_flows_data:
        for flow in message_flows_data.get('children', []):
            flow_details = api_client.fetch_uri(flow['uri'])
            if flow_details:
                active_data = flow_details['active']
                metrics_handler.update_thread_metrics(
                    server_name,
                    app_name,
                    flow['name'],
                    active_data.get('threads', 0),
                    active_data.get('threadsCapacity', 0),
                    active_data.get('threadsDemanded', 0),
                    active_data.get('threadsInUse', 0)
                )

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
