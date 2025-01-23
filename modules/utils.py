from dotenv import load_dotenv
from os import getenv
from .pyMongo import MongoDB
from .websocks import MQTTWebSocketClient

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