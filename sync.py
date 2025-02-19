import psycopg2
import json
from utils import send_discord_notification
from mikrotik.add import add_wireguard_peer_to_mikrotik
from mikrotik.delete import delete_wireguard_peer
from mikrotik.get import get_wireguard_status

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

INTERFACE = config["mikrotik"]["interface"]
DISCORD_WEBHOOK = config["discord_webhook"]
DB_CONFIG = config["database"]

def sync_wireguard():
    try:
        # Koneksi ke PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        cursor = conn.cursor()

        # Ambil data dari database
        cursor.execute("SELECT name, public_key, allowed_ip FROM wireguard_peers")
        db_peers = cursor.fetchall()

        # Ambil daftar peer yang ada di WireGuard
        wg_peers = get_wireguard_status()
        wg_peer_keys = {(peer["public-key"], peer["name"]) for peer in wg_peers}

        # Sinkronisasi: Tambah peer baru, hapus peer lama
        db_peer_keys = {(peer[1], peer[0]) for peer in db_peers}  # Menggunakan name sebagai kunci

        # # Tambah peer yang belum ada di WireGuard
        for name, public_key, allowed_ip in db_peers:
            if (public_key, name) not in wg_peer_keys:
                add_wireguard_peer_to_mikrotik(name, public_key, allowed_ip, INTERFACE)
                print("CUK MASUK SINI GA")

        # Hapus peer yang tidak ada di database
        for peer in wg_peers:
            if (peer["public-key"], peer["name"]) not in db_peer_keys:
                delete_wireguard_peer(peer["public-key"], peer["name"], INTERFACE)

        conn.close()

        # Kirim notifikasi
        if DISCORD_WEBHOOK:
            send_discord_notification("✅ Sinkronisasi WireGuard selesai.")

    except Exception as e:
        print(f"Error: {e}")
        if DISCORD_WEBHOOK:
            send_discord_notification(f"⚠️ Gagal melakukan sinkronisasi WireGuard: {e}")

if __name__ == "__main__":
    sync_wireguard()