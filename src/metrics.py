from prometheus_client import Gauge, generate_latest, REGISTRY

class MetricsHandler:
    def __init__(self):
        self.application_count = Gauge('ace_application_count', 'Number of applications', ['server'])
        self.rest_api_count = Gauge('ace_rest_api_count', 'Number of REST APIs', ['server'])

    def update_metrics(self, server_name, app_count, api_count):
        self.application_count.labels(server=server_name).set(app_count)
        self.rest_api_count.labels(server=server_name).set(api_count)

    def get_metrics(self):
        return generate_latest(REGISTRY)
