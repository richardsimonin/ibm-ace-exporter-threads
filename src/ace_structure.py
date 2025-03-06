from datetime import datetime
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class ACEStructure:
    def __init__(self):
        self.servers = {}
        self.last_update = None
        self.lock = threading.Lock()

    def update_structure(self, api_client):
        new_servers = {}
        servers_data = api_client.fetch_uri("/apiv2/servers")
        if servers_data:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_server = {executor.submit(self.process_server, api_client, server): server for server in servers_data.get('children', [])}
                for future in as_completed(future_to_server):
                    server = future_to_server[future]
                    try:
                        server_data = future.result()
                        new_servers[server['name']] = server_data
                    except Exception as exc:
                        print(f"Processing server {server['name']} generated an exception: {exc}")
        
        with self.lock:
            self.servers = new_servers
            self.last_update = datetime.now()

    def process_server(self, api_client, server):
        server_data = {'applications': {}}
        server_details = api_client.fetch_uri(server['uri'])
        if server_details:
            applications_uri = server_details['children']['applications']['uri']
            applications_data = api_client.fetch_uri(applications_uri)
            if applications_data:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_app = {executor.submit(self.process_application, api_client, app): app for app in applications_data.get('children', [])}
                    for future in as_completed(future_to_app):
                        app = future_to_app[future]
                        try:
                            app_data = future.result()
                            server_data['applications'][app['name']] = app_data
                        except Exception as exc:
                            print(f"Processing application {app['name']} generated an exception: {exc}")
        return server_data

    def process_application(self, api_client, app):
        app_data = {'message_flows': []}
        app_details = api_client.fetch_uri(app['uri'])
        if app_details:
            message_flows_uri = app_details['children']['messageFlows']['uri']
            message_flows_data = api_client.fetch_uri(message_flows_uri)
            if message_flows_data:
                for flow in message_flows_data.get('children', []):
                    app_data['message_flows'].append({
                        'name': flow['name'],
                        'uri': flow['uri']
                    })
        return app_data

    def get_structure(self):
        with self.lock:
            return self.servers.copy()
