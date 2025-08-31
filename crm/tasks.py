import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

from celery import shared_task

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/"

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    format="%(message)s"
)

transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
    query {
        totalRevenue
        totalOrders
        totalCustomers
    }
""")

@shared_task
def generate_crm_report():
    try:
        response = client.execute(query)
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        message = f"{now} - Report: {response.get('totalCustomers', 0)} customers, {response.get('totalOrders', 0)} orders, {response.get('totalRevenue', 0)} revenue"

        with open(LOG_FILE, "a") as log_file:
            log_file.write(message)

        return response
    except Exception as e:
        logging.error(f"Error generating CRM report: {e}")
        return {"Details": str(e)}
