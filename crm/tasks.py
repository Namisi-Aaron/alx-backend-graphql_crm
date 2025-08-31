import requests
import logging
from datetime import datetime
from celery import shared_task

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/"

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    format="%(message)s"
)

query = """
    query {
        totalRevenue
        totalOrders
        totalCustomers
    }
"""

@shared_task
def generate_crm_report():
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json={"query": query},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json().get("data", {})

        total_customers = data.get("totalCustomers", 0)
        total_orders = data.get("totalOrders", 0)
        total_revenue = data.get("totalRevenue", 0)

        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        message = f"{now} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"

        logging.info(message)
        return {"success": True, "message": message}

    except Exception as e:
        logging.error(f"Error generating CRM report: {e}")
        return {"success": False, "Details": str(e)}
