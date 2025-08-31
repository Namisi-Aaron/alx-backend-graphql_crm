import datetime

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """
    Log the CRM heartbeat status.
    """
    now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"
    
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message)
