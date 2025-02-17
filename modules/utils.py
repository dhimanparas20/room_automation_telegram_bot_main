from dotenv import load_dotenv
from os import getenv,popen
from .pyMongo import MongoDB
from .websocks import MQTTWebSocketClient
import speedtest
import shutil
import platform
import subprocess

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = int(getenv('API_ID'))
API_HASH = getenv('API_HASH')

# Mongo Configuration
CONNECTION_STRING = getenv('CONNECTION_STRING')
DB_NAME = "tgautomation"
COLLECTION_NAME = "users"

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


# Function to get system usage without psutil
def get_system_usage():
    # Get CPU usage percentage using `os` and `subprocess`
    if platform.system() == "Linux":
        cpu_usage = subprocess.check_output(
            ["sh", "-c", "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"]
        ).decode().strip()
    else:
        cpu_usage = "N/A (only supported on Linux)"

    # Get RAM usage information using `os`
    try:
        ram_info = popen("free -m").readlines()[1].split()
        total_memory = int(ram_info[1])
        used_memory = int(ram_info[2])
        ram_usage_percent = int((used_memory / total_memory) * 100)  # Convert to integer
    except IndexError:
        ram_usage_percent = "N/A"

    # Get disk usage information using `shutil`
    total, used, free = shutil.disk_usage("./")
    disk_usage_percent = int((used / total) * 100)  # Convert to integer

    # Format the results
    results = {
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage_percent,  # Integer value
        "disk_usage_percent": disk_usage_percent,  # Integer value
        "disk_used_space": get_file_size(used),
        "disk_total_space": get_file_size(total),
        "disk_available_space": get_file_size(free),
    }

    return results

# Helper function to format file size
def get_file_size(size_in_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"

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
