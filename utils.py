import requests
import json

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

DISCORD_WEBHOOK = config["discord_webhook"]

def send_discord_notification(message):
    """Mengirim notifikasi ke Discord menggunakan webhook."""
    if DISCORD_WEBHOOK:
        payload = {"content": message}
        try:
            response = requests.post(DISCORD_WEBHOOK, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Gagal mengirim notifikasi ke Discord: {e}")

if __name__ == "__main__":
    send_discord_notification("🔔 Notifikasi test dari WireGuard Sync!")

