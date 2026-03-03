import socket
import json
import matplotlib.pyplot as plt      
from matplotlib.animation import FuncAnimation
import numpy as np  # Wichtig: Oben importieren!

# --- NETZWERK SETUP ---
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False) 

# --- MATPLOTLIB SETUP ---
# Hier wird das Fenster erstellt
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 1280)
ax.set_ylim(720, 0) # Y-Achse spiegeln, damit es wie im Video aussieht
ax.set_title("Live Hand-Tracking Daten")

# Scatter-Objekte für bis zu 2 Hände
scatters = [ax.scatter([], [], c='blue', label='Hand Links'), 
            ax.scatter([], [], c='red', label='Hand Rechts')]

def update(frame):
    try:
        # Puffer leeren, um immer das aktuellste Bild zu haben
        data = None
        while True:
            try:
                data, addr = sock.recvfrom(4096)
            except BlockingIOError:
                break
        
        if data:
            hands = json.loads(data.decode())
            
            # Erstmal alle Punkte "unsichtbar" machen
            for s in scatters:
                s.set_offsets(np.empty((0, 2)))

            # Neue Punkte setzen
            for i, hand in enumerate(hands):
                if i < len(scatters):
                    points = np.array(hand["points"])
                    scatters[i].set_offsets(points)
    except Exception as e:
        pass # Wenn mal kein Paket kommt, einfach weitermachen
    
    return scatters

# Das Intervall (ms) bestimmt, wie oft das Fenster aktualisiert wird
ani = FuncAnimation(fig, update, interval=10, blit=True, cache_frame_data=False)

plt.legend()
plt.show() # Dieser Befehl ÖFFNET das Fenster