import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "https://http://127.0.0.1:8000/graphql"
LOG_FILE = "/tmp/crm_heartbeat_log.txt"

transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
    query {
        hello
    }
""")

def log_crm_heartbeat():
    """
    Log the CRM heartbeat status.
    """
    try:
        response = client.execute(query)
        
        now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        message = f"{now} CRM is alive\n"
        
        with open(LOG_FILE, "a") as log_file:
            log_file.write(message)
        
        print(response)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    log_crm_heartbeat()
