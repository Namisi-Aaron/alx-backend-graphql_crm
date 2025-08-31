import logging
from datetime import datetime, timedelta
from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# ------------------ CONFIG ------------------
GRAPHQL_ENDPOINT = "https://http://127.0.0.1:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

# ------------------ SETUP LOGGING ------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ GRAPHQL SETUP ------------------
transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# ------------------ QUERY ------------------
query = gql("""           
query {
  allOrders {
    id
    customerId {
      email
    }
    orderDate
  }
}
""")

def fetch_recent_orders():
    try:
        response = client.execute(query)
        orders = response.get("allOrders", [])

        cutoff_date = timezone.now() - timedelta(days=7)

        for order in orders:
            order_date = datetime.fromisoformat(order["orderDate"])
            if order_date >= cutoff_date:
                order_id = order["id"]
                customer_email = order["customerId"]["email"]
                logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_recent_orders()
