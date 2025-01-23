from dotenv import load_dotenv
from os import getenv
from .pyMongo import MongoDB
from .websocks import MQTTWebSocketClient
import speedtest
import psutil
import time

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = int(getenv('API_ID'))
API_HASH = getenv('API_HASH')

# Mongo Configuration
CONNECTION_STRING = getenv('CONNECTION_STRING')
DB_NAME = getenv('DB_NAME')
COLLECTION_NAME = getenv('COLLECTION_NAME')

# MQTT Configuration
WEBSOCK_BROKER_ADDRESS = getenv('WEBSOCK_BROKER_ADDRESS')
WEBSOCK_PORT = int(getenv('WEBSOCK_PORT'))
WEBSOCK_USE_SSL = getenv('WEBSOCK_USE_SSL').lower() == 'true'
CLEAN_SESSION = getenv('CLEAN_SESSION',"true").lower() == 'true'
USE_CREDS = getenv('USE_CREDS',"true").lower() == 'true'
RETAINED = getenv('RETAINED',"true").lower() == 'true'
MQTT_USER = getenv('MQTT_USER')
MQTT_PASS = getenv('MQTT_PASS')
QOS = int(getenv('QOS'))
PINS = getenv('PINS').split(",")

# Initialize Mongo DB Client
mongoClient = MongoDB(db_name=DB_NAME,collection_name=COLLECTION_NAME,connection_str=CONNECTION_STRING)

# Initialize MQTT WebSocket Client
mqtt_client = MQTTWebSocketClient(
    host=WEBSOCK_BROKER_ADDRESS,
    port=WEBSOCK_PORT,
    username=MQTT_USER,
    password=MQTT_PASS,
    use_ssl=WEBSOCK_USE_SSL,
    clean_session=CLEAN_SESSION,
    retained=RETAINED,
    qos=QOS,
    use_creds=USE_CREDS
)
mqtt_client.connect()

#Sorts File Size units
def get_file_size(bytes):
    bytes = int(bytes)
    if bytes < 1024:
        return bytes,"B"
    elif bytes >= 1024 and bytes < 1024*1024:
        return f"{bytes/1024:.1f} KB"
    elif bytes >= 1024*1024 and bytes < 1024*1024*1024:
        return f"{bytes/(1024*1024):.1f} MB"
    else:
        return f"{bytes/(1024*1024*1024):.1f} GB"

# Function to get system usage
def get_system_usage():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=0)
    
    # Get RAM usage information
    memory_info = psutil.virtual_memory()
    ram_usage = memory_info.percent
    
    # Get disk usage information
    disk_usage = psutil.disk_usage("./")
    disk_usage_percent = disk_usage.percent
    disk_used = disk_usage.used
    disk_total = disk_usage.total
    disk_available = disk_usage.free

    # Format the results
    results = {
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage,
        "disk_usage_percent": disk_usage_percent,
        "disk_used_space": get_file_size(disk_used),
        "disk_total_space": get_file_size(disk_total),
        "disk_available_space": get_file_size(disk_available)
    }
    
    return results  

# Perform SpeedTest
def perform_speedtest():
    st = speedtest.Speedtest()
    st.get_servers()
    st.get_best_server()
    download_speed = st.download()
    upload_speed = st.upload()
    ping = st.results.ping
    return {
        'download_speed': download_speed,
        'upload_speed': upload_speed,
        'ping': ping
    }