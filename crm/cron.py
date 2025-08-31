import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "https://http://127.0.0.1:8000/graphql"


transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

def log_crm_heartbeat():
    """
    Log the CRM heartbeat status.
    """
    LOG_FILE = "/tmp/crm_heartbeat_log.txt"
    try:
        query = gql("""
            query {
                hello
            }
        """)
        response = client.execute(query)
        
        now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        message = f"{now} CRM is alive\n"
        
        with open(LOG_FILE, "a") as log_file:
            log_file.write(message)
        
        print(response)
    
    except Exception as e:
        print(f"Error: {e}")

def update_low_stock():
    """
    Update products with low stock.
    """
    LOG_FILE = "/tmp/low_stock_updates_log.txt"
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                products
            }
        }
    """)

    try:
        response = client.execute(mutation)
        now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        message = f'''
            {now} Low stock products updated: {response.get('data', {}).get('updateLowStockProducts', {}).get('products', [])}
        '''

        with open(LOG_FILE, "a") as log_file:
            log_file.write(message)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
