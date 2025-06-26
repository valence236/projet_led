import socket

# 🔧 Paramètres Art-Net
target_ip = "192.168.1.45"     # IP du contrôleur BC216
universe = 0                   # Univers à tester
num_leds = 170                 # 170 LEDs RGB = 510 canaux
port = 6454

# 🎨 Générer les données DMX en bleu (R=0, G=0, B=255)
data = []
for _ in range(num_leds):
    data += [0, 0, 255]  # Bleu

# Remplir les 512 canaux
dmx_data = data[:512]
dmx_data += [0] * (512 - len(dmx_data))

# 🔧 Créer le paquet Art-Net
packet = bytearray()
packet.extend(b'Art-Net\x00')                      # Header
packet.extend((0x00, 0x50))                        # OpCode ArtDMX
packet.extend((0x00, 14))                          # Protocol version
packet.append(0x00)                                # Sequence
packet.append(0x00)                                # Physical
packet.extend((universe & 0xFF, (universe >> 8)))  # Univers LSB/MSB
packet.extend((len(dmx_data) >> 8, len(dmx_data) & 0xFF))  # Length
packet.extend(dmx_data)                            # Données DMX

# 📤 Envoyer via UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(packet, (target_ip, port))
sock.close()

print(f"✅ {num_leds} LEDs allumées en bleu sur l'univers {universe}")