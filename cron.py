import time
import threading
import json
from sync import sync_wireguard_peers
from status import get_wireguard_status

with open("config.json", "r") as f:
    config = json.load(f)

SYNC_INTERVAL = config["sync_interval"]
STATUS_INTERVAL = config["status_interval"]

def load_cron_status():
    try:
        with open("cron_status.json", "r") as f:
            return json.load(f)["enabled"]
    except FileNotFoundError:
        return False

def sync_job():
    while load_cron_status():
        print("\n🔄 Menjalankan sinkronisasi otomatis...")
        sync_wireguard_peers()
        time.sleep(SYNC_INTERVAL)

def status_job():
    while load_cron_status():
        print("\n🔍 Mengecek status WireGuard otomatis...")
        get_wireguard_status()
        time.sleep(STATUS_INTERVAL)

def start_cron():
    if load_cron_status():
        threading.Thread(target=sync_job, daemon=True).start()
        threading.Thread(target=status_job, daemon=True).start()
        print("✅ Cron job AKTIF!")

if __name__ == "__main__":
    print("🔄 Memeriksa status cron...")
    start_cron()
    while True:
        time.sleep(1)
