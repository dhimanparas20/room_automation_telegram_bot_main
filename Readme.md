
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
git clone https://github.com/dhimanparas20/room_automation_telegram_bot_main
cd room_automation_telegram_bot
```

### Setup Environment Variables
1. Rename `env_sample` to `.env`:
   ```bash
   mv env_sample .env
   ```
2. Fill in the required environment variables in the `.env` file:
   ```env
   # Telegram API Configuration
   BOT_TOKEN=
   API_ID=
   API_HASH=

   # MQTT Configuration
   WEBSOCK_BROKER_ADDRESS=
   WEBSOCK_PORT=
   WEBSOCK_USE_SSL=true
   USE_CREDS=true
   MQTT_USER=
   MQTT_PASS=
   PINS=D1,D2,D3,D4
   QOS=1
   CLEAN_SESSION=true
   RETAINED=true

   # MongoDB Configuration
   CONNECTION_STRING=
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
| `/speedtest`     | Do a Server Speedtest                      |
| `/stats`         | Get Server Stats                           |
| `d1 <0/1>`       | Toggle device D1 (0 = off, 1 = on).        |
| `d2 <0/1>`       | Toggle device D2 (0 = off, 1 = on).        |
| `d3 <0/1>`       | Toggle device D3 (0 = off, 1 = on).        |
| `d4 <0/1>`       | Toggle device D4 (0 = off, 1 = on).        |

---

I'll help you enhance the README with a CI/CD section focusing on GitHub Actions. Here's a comprehensive addition:

---

## CI/CD Pipeline Configuration

### GitHub Actions Workflow

The provided GitHub Actions workflow enables automatic deployment with the following environment variables:

#### Required GitHub Secrets

1. `SSH_HOST`: Server's IP address or hostname
2. `SSH_USER`: SSH username for server access
3. `SSH_PASSWORD`: SSH password or passphrase
4. `WORK_DIR`: Full path to the project directory on the remote server
5. `MAIN_BRANCH`: Git branch to pull (typically `main`)

#### Setup Steps

1. Navigate to your GitHub repository's Settings
2. Select "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add each secret with its corresponding value:
   - `SSH_HOST`: example.com
   - `SSH_USER`: your_username
   - `SSH_PASSWORD`: your_ssh_password
   - `WORK_DIR`: /path/to/project
   - `MAIN_BRANCH`: main

#### Workflow Execution

The workflow can be triggered:
- Manually via "workflow_dispatch"
- Uncomment push triggers for automatic deployment on code changes

#### Workflow Steps
1. Installs `sshpass`
2. Connects to remote server
3. Pulls latest code
4. Rebuilds Docker containers
5. Restarts services
6. Prunes unused Docker images

### Best Practices

- Use SSH keys instead of passwords for enhanced security
- Implement branch protection rules
- Configure separate workflows for testing and deployment

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
