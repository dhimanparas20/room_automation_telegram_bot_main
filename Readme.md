
# Room Automation Telegram Bot

This is a Python-based Telegram bot using the Pyrogram client, designed to trigger and control your room automation setup via MQTT. The bot provides an easy way to manage devices in your setup directly through Telegram commands.

---

## Features
- Trigger room automation devices via MQTT.
- Attach, update, and revoke tokens associated with devices.
- Control devices D1, D2, D3, and D4 by toggling their state (on/off).
- Sends a notification when the bot is online.

---

## Getting Started

### Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### Setup Environment Variables
1. Rename `env_sample` to `.env`:
   ```bash
   mv env_sample .env
   ```
2. Fill in the required environment variables in the `.env` file:
   ```env
   # Telegram API Configuration
   BOT_TOKEN=6606146224:AAHs2D5D7o3aCCJl7TWhL9wovCmXN0QWZXA
   API_ID=2639179
   API_HASH=7e40ff5b5676e9f355ec4b610abb09a1

   # MQTT Configuration
   WEBSOCK_BROKER_ADDRESS=mqtt.mstservices.tech
   WEBSOCK_PORT=443
   WEBSOCK_USE_SSL=true
   USE_CREDS=true
   MQTT_USER=mst
   MQTT_PASS=1212
   PINS=D1,D2,D3,D4
   QOS=1
   CLEAN_SESSION=true
   RETAINED=true

   # MongoDB Configuration
   CONNECTION_STRING=mongodb+srv://ken:2069@automation.tl2hwga.mongodb.net/?retryWrites=true&w=majority&appName=Automation
   DB_NAME=tgautomation
   COLLECTION_NAME=users
   ```

---

## Running the Project

### Using Docker

1. Build and run the Docker container:
   ```bash
   docker build -t room-automation-bot .
   docker run -d --env-file .env --name tg_bot_service room-automation-bot
   ```

### Using Docker Compose
1. Run the project using Docker Compose:
   ```bash
   docker-compose up -d
   ```

---

### Manual Setup

1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python app.py
   ```

---

## Bot Commands

| Command          | Description                                |
|-------------------|--------------------------------------------|
| `/settoken`      | Attach or update a token (requires token). |
| `/gettoken`      | Displays all attached tokens.              |
| `/revoketoken`   | Detaches all tokens.                       |
| `d1 <0/1>`       | Toggle device D1 (0 = off, 1 = on).        |
| `d2 <0/1>`       | Toggle device D2 (0 = off, 1 = on).        |
| `d3 <0/1>`       | Toggle device D3 (0 = off, 1 = on).        |
| `d4 <0/1>`       | Toggle device D4 (0 = off, 1 = on).        |

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contribution

Feel free to contribute to this project by submitting issues or pull requests.

---

## Acknowledgements

- Telegram API for providing an easy way to interact with users.
- Pyrogram for the efficient and lightweight Telegram client.
- MQTT for enabling seamless communication between devices.

---

### Disclaimer

This project is provided "as is" without any warranty. Use it at your own risk.
