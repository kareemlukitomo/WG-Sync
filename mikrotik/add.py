import paramiko
import json
import os
import psycopg2

# Load konfigurasi
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

MIKROTIK_CONFIG = config["mikrotik"]
DB_CONFIG = config["database"]

def add_wireguard_peer_to_mikrotik(name, public_key, allowed_ip, interface):
    """Menambahkan peer WireGuard ke MikroTik melalui SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"🔄 Menambahkan peer WireGuard ke MikroTik {MIKROTIK_CONFIG['host']}...")
        ssh.connect(
            hostname=MIKROTIK_CONFIG["host"],
            port=MIKROTIK_CONFIG["port"],
            username=MIKROTIK_CONFIG["user"],
            password=MIKROTIK_CONFIG["password"]
        )

        command = f'/interface/wireguard/peers/add name={name} public-key={public_key} allowed-address={allowed_ip} comment={name} interface={interface}'
        ssh.exec_command(command)

    except Exception as e:
        raise Exception(f"Gagal menambahkan peer ke MikroTik: {e}")
    finally:
        ssh.close()