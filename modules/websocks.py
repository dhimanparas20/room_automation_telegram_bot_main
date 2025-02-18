import paho.mqtt.client as mqtt
import json
import ssl
import asyncio

class MQTTWebSocketClient:
    def __init__(self, host, port, username, password, use_ssl=True, qos=0, clean_session=True, retained=False, use_creds=True, message_callback=None):
        """
        Initialize MQTT WebSocket Client
        """
        self.qos = qos
        self.retained = retained
        self.clean_session = clean_session
        self.message_callback = message_callback

        self.buttons = ["D1", "D2", "D3", "D4", "online"]
        self.host = host
        self.port = port

        self.client = mqtt.Client(
            client_id="python_websocket_client",
            transport="websockets",
            clean_session=self.clean_session
        )

        # Set credentials
        if use_creds:
            self.client.username_pw_set(username, password)

        # SSL/TLS Configuration
        if use_ssl:
            self.client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)
            self.client.tls_insecure_set(True)

        # Event loop setup
        self.loop = asyncio.get_running_loop()
        self.queue = asyncio.Queue()  # Message queue for async processing

        # Store subscribed topics and their latest values
        self.topic_values = {}

        # MQTT Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        # self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

    async def connect(self):
        """
        Establish async connection to MQTT broker
        """
        try:
            print(f"Connecting to {self.host}:{self.port}")
            self.client.connect(self.host, self.port, keepalive=60)
            self.client.loop_start()  # Start the MQTT loop
        except Exception as e:
            print(f"Connection Error: {e}")

    async def disconnect(self):
        """
        Disconnect from MQTT broker asynchronously
        """
        self.client.loop_stop()
        self.client.disconnect()

    async def update_topic_value(self, topic, value):
        """
        Update value of a specific topic asynchronously
        """
        button = topic.split("/")
        if button[1] in self.buttons:
            self.client.publish(topic, str(value), qos=self.qos, retain=self.retained)

    def on_connect(self, client, userdata, flags, rc):
        """
        Connection callback
        """
        if rc == 0:
            print("Connected successfully")
        else:
            print(f"Connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        """
        Disconnection callback
        """
        print(f"Disconnected with code {rc}")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        Subscription callback
        """
        print("Subscribed to topics successfully")

    def set_message_callback(self, callback):
        """
        Set the message callback dynamically
        """
        self.message_callback = callback

    def on_message(self, client, userdata, message):
        """
        Handle received messages and send them to the async queue
        """
        topic = message.topic
        payload = message.payload.decode('utf-8')

        if payload in ['0', '1']:
            print(f"Received on {topic}: {payload}")

            # Store the latest value for the topic
            self.topic_values[topic] = payload

            if self.message_callback:
                asyncio.run_coroutine_threadsafe(self.message_callback(topic, payload), self.loop)

    async def get_topic_values(self):
        """
        Retrieve the latest values of all subscribed topics asynchronously
        """
        return json.dumps(self.topic_values, indent=2)

    async def subscribe_to_online_topic(self, token):
        """
        Subscribe to a specific online topic asynchronously
        """
        topic = f"{token}/online"
        self.client.subscribe(topic, qos=self.qos)
        self.topic_values[topic] = None  # Initialize with None before data arrives
        print(f"Subscribed to {topic} with QoS {self.qos}")

    async def unsubscribe_topics(self, token):
        """
        Unsubscribe from topics asynchronously
        """
        topics = [
            f"{token}/D1",
            f"{token}/D2",
            f"{token}/D3",
            f"{token}/D4",
            f"{token}/online"
        ]
        for topic in topics:
            self.client.unsubscribe(topic)
            self.topic_values.pop(topic, None)  # Remove topic from stored values
            print(f"Unsubscribed from {topic}")
