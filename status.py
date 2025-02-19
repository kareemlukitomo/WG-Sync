import json
import requests
from utils import send_discord_notification
from mikrotik.get import get_wireguard_status, get_total_peers  # Impor fungsi dari mikrotik/get.py

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

DISCORD_WEBHOOK = config["discord_webhook"]
INTERFACE = config["mikrotik"]["interface"]

def check_status():
    try:
        # Dapatkan status WireGuard dari MikroTik
        status_output = get_wireguard_status()

        # Parsing hasil
        status_lines = status_output.strip().split("\n")
        peers = [line.split() for line in status_lines]

        # Format hasil
        formatted_status = "\n".join(
            [f"Peer: {peer[0]}, Last Handshake: {peer[4]}" for peer in peers]
        )

        print("WireGuard Status:\n", formatted_status)

        # Dapatkan total peers dari MikroTik
        total_peers = get_total_peers(INTERFACE)
        print(f"Total Peers: {total_peers}")

        # Kirim notifikasi ke Discord jika webhook diatur
        if DISCORD_WEBHOOK:
            send_discord_notification(f"Total Peers: {total_peers}")

    except Exception as e:
        print(f"Error: {e}")
        if DISCORD_WEBHOOK:
            send_discord_notification(f"⚠️ Gagal mengecek status WireGuard: {e}")

if __name__ == "__main__":
    check_status()