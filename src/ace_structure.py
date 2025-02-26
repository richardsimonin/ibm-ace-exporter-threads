from datetime import datetime
from threading import Lock

class ACEStructure:
    def __init__(self):
        self.servers = {}
        self.last_update = None
        self.lock = Lock()

    def update_structure(self, api_client):
        self.servers = {}
        servers_data = api_client.fetch_uri("/apiv2/servers")
        if servers_data:
            for server in servers_data.get('children', []):
                server_name = server['name']
                self.servers[server_name] = {'applications': {}}
                server_details = api_client.fetch_uri(server['uri'])
                if server_details:
                    applications_uri = server_details['children']['applications']['uri']
                    applications_data = api_client.fetch_uri(applications_uri)
                    if applications_data:
                        for app in applications_data.get('children', []):
                            app_name = app['name']
                            self.servers[server_name]['applications'][app_name] = {'message_flows': []}
                            app_details = api_client.fetch_uri(app['uri'])
                            if app_details:
                                message_flows_uri = app_details['children']['messageFlows']['uri']
                                message_flows_data = api_client.fetch_uri(message_flows_uri)
                                if message_flows_data:
                                    for flow in message_flows_data.get('children', []):
                                        self.servers[server_name]['applications'][app_name]['message_flows'].append({
                                            'name': flow['name'],
                                            'uri': flow['uri']
                                        })
        self.last_update = datetime.now()

    def get_structure(self):
        with self.lock:
            return self.servers.copy()
