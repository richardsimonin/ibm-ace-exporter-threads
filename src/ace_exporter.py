from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from flask import Flask, Response
from api_client import APIClient
from metrics import MetricsHandler
import threading
import time
import os
from ace_structure import ACEStructure
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
api_client = APIClient(
    os.environ.get('ACE_URL'),
    os.environ.get('ACE_USERNAME'),
    os.environ.get('ACE_PASSWORD')
)
metrics_handler = MetricsHandler()
ace_structure = ACEStructure()

def update_structure():
    while True:
        logging.info("Début de la mise à jour de la structure")
        ace_structure.update_structure(api_client)
        logging.info(f"Structure mise à jour à {ace_structure.last_update}")
        time.sleep(300)  # Mise à jour toutes les 5 minutes

def update_metrics():
    while True:
        start_time = datetime.now()
        logging.info(f"Début du processus de mise à jour des métriques à {start_time}")
        
        structure = ace_structure.get_structure()
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for server_name, server_data in structure.items():
                for app_name, app_data in server_data['applications'].items():
                    for flow in app_data['message_flows']:
                        futures.append(executor.submit(process_flow_metrics, api_client, server_name, app_name, flow))
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    logging.error(f"Une erreur s'est produite lors de la mise à jour des métriques : {exc}")
        
        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"Fin du processus de mise à jour des métriques à {end_time}. Durée : {duration}")
        
        time.sleep(15)  # Mise à jour toutes les 15 secondes

def process_flow_metrics(api_client, server_name, app_name, flow):
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


@app.route('/metrics')
def metrics():
    return Response(metrics_handler.get_metrics(), mimetype='text/plain')

if __name__ == '__main__':
    structure_thread = threading.Thread(target=update_structure)
    metrics_thread = threading.Thread(target=update_metrics)
    structure_thread.start()
    metrics_thread.start()
    app.run(host='0.0.0.0', port=8000)
