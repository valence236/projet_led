import socket
import time

def send_artnet_packet(ip, universe, dmx_data):
    packet = bytearray()
    packet.extend(b'Art-Net\x00')
    packet.extend((0x00, 0x50))  # OpCode ArtDMX
    packet.extend((0x00, 14))   # Protocol version
    packet.append(0x00)         # Sequence
    packet.append(0x00)         # Physical
    packet.extend((universe & 0xFF, (universe >> 8)))  # Universe
    packet.extend((len(dmx_data) >> 8, len(dmx_data) & 0xFF))  # Length
    packet.extend(dmx_data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip, 6454))
    sock.close()

# Couleurs
YELLOW_RGB = [255, 255, 0]
OFF_RGB = [0, 0, 0]

# Chaque bande = 2 univers → 170 + 89 LEDs
def get_led_count_for_universe(index):
    return 170 if index % 2 == 0 else 89

# Configuration des 4 contrôleurs
controllers = [
    {"ip": "192.168.1.45", "universe_start": 0,   "universe_end": 31},
    {"ip": "192.168.1.46", "universe_start": 32,  "universe_end": 63},
    {"ip": "192.168.1.47", "universe_start": 64,  "universe_end": 95},
    {"ip": "192.168.1.48", "universe_start": 96,  "universe_end": 127},
]

# 🔆 Allume toutes les LEDs en jaune
for controller in controllers:
    ip = controller["ip"]
    for universe_index, universe in enumerate(range(controller["universe_start"], controller["universe_end"] + 1)):
        led_count = get_led_count_for_universe(universe_index)
        data = YELLOW_RGB * led_count
        dmx_data = data + [0] * (512 - len(data))
        send_artnet_packet(ip, universe, dmx_data)
        print(f"✅ {led_count} LEDs JAUNES → {ip} univers {universe}")

# Pause d'affichage
time.sleep(5)


# 🚫 Éteint toutes les LEDs
print("🕶️ Extinction des LEDs...")
for controller in controllers:
    ip = controller["ip"]
    for universe_index, universe in enumerate(range(controller["universe_start"], controller["universe_end"] + 1)):
        led_count = get_led_count_for_universe(universe_index)
        data = OFF_RGB * led_count
        dmx_data = data + [0] * (512 - len(data))
        send_artnet_packet(ip, universe, dmx_data)
        print(f"❌ {led_count} LEDs ÉTEINTES → {ip} univers {universe}")
