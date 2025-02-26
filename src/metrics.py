from prometheus_client import Gauge, generate_latest, REGISTRY

class MetricsHandler:
    def __init__(self):
        self.threads = Gauge('ace_threads', 'Number of threads', ['server', 'application', 'message_flow'])
        self.threads_capacity = Gauge('ace_threads_capacity', 'Thread capacity', ['server', 'application', 'message_flow'])
        self.threads_demanded = Gauge('ace_threads_demanded', 'Threads demanded', ['server', 'application', 'message_flow'])
        self.threads_in_use = Gauge('ace_threads_in_use', 'Threads in use', ['server', 'application', 'message_flow'])

    def update_thread_metrics(self, server, application, message_flow, threads, threads_capacity, threads_demanded, threads_in_use):
        self.threads.labels(server=server, application=application, message_flow=message_flow).set(threads)
        self.threads_capacity.labels(server=server, application=application, message_flow=message_flow).set(threads_capacity)
        self.threads_demanded.labels(server=server, application=application, message_flow=message_flow).set(threads_demanded)
        self.threads_in_use.labels(server=server, application=application, message_flow=message_flow).set(threads_in_use)

    def get_metrics(self):
        return generate_latest(REGISTRY)
