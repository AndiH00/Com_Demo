import socket
import threading
import tkinter as tk
from tkinter import messagebox

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024


class UDPClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Client")

        self.sock = None
        self.running = False

        self._build_gui()

    def _build_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(frame, text="Nicht verbunden", fg="red")
        self.status_label.grid(row=0, column=0, columnspan=3, sticky="w")

        self.btn_connect = tk.Button(frame, text="Verbinden", command=self.connect)
        self.btn_connect.grid(row=1, column=0, pady=5, sticky="ew")

        self.btn_disconnect = tk.Button(frame, text="Trennen", command=self.disconnect, state=tk.DISABLED)
        self.btn_disconnect.grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="X:").grid(row=2, column=0, sticky="e")
        self.entry_x = tk.Entry(frame, width=8)
        self.entry_x.grid(row=2, column=1, sticky="w")

        tk.Label(frame, text="Y:").grid(row=3, column=0, sticky="e")
        self.entry_y = tk.Entry(frame, width=8)
        self.entry_y.grid(row=3, column=1, sticky="w")

        self.btn_status = tk.Button(frame, text="Status", command=self.send_status, state=tk.DISABLED)
        self.btn_status.grid(row=4, column=0, pady=5, sticky="ew")

        self.btn_pos = tk.Button(frame, text="X-Y-Position", command=self.send_position, state=tk.DISABLED)
        self.btn_pos.grid(row=4, column=1, pady=5, sticky="ew")

        self.btn_stop = tk.Button(frame, text="Stop", command=self.send_stop, state=tk.DISABLED)
        self.btn_stop.grid(row=4, column=2, pady=5, sticky="ew")

        self.text_log = tk.Text(frame, height=12, width=60, state=tk.DISABLED)
        self.text_log.grid(row=5, column=0, columnspan=3, pady=5)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

    # ---------------- UDP ----------------

    def connect(self):
        if self.sock:
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

        self.running = True
        threading.Thread(target=self._receive_loop, daemon=True).start()

        self.status_label.config(text="Verbunden", fg="green")
        self.btn_connect.config(state=tk.DISABLED)
        self.btn_disconnect.config(state=tk.NORMAL)
        self.btn_status.config(state=tk.NORMAL)
        self.btn_pos.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.NORMAL)

        self._log("UDP Socket geöffnet.")

    def disconnect(self):
        if not self.sock:
            return

        self.running = False
        self.sock.close()
        self.sock = None

        self.status_label.config(text="Nicht verbunden", fg="red")
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)
        self.btn_status.config(state=tk.DISABLED)
        self.btn_pos.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.DISABLED)

        self._log("UDP Socket geschlossen.")

    def _receive_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                msg = data.decode("utf-8").strip()
                self._handle_incoming(msg, addr)
            except BlockingIOError:
                pass

    # ---------------- Empfangslogik ----------------

    def _handle_incoming(self, msg, addr):
        parts = msg.split()

        if len(parts) == 0:
            return

        cmd = parts[0].upper()

        if cmd == "STATUS":
            self._log(f"STATUS vom Server: {' '.join(parts[1:])}")

        elif cmd == "POSITION" and len(parts) >= 3:
            x, y = parts[1], parts[2]
            self._log(f"POSITION empfangen: X={x}, Y={y}")

        elif cmd == "HEARTBEAT":
            self._log("Heartbeat empfangen (100ms)")

        else:
            self._log(f"Unbekanntes Paket: {msg}")

    # ---------------- Senden ----------------

    def _send(self, text: str):
        if not self.sock:
            messagebox.showwarning("Nicht verbunden", "Bitte zuerst verbinden.")
            return

        self.sock.sendto(text.encode("utf-8"), (UDP_IP, UDP_PORT))
        self._log(f"Sende: {text}")

    def send_status(self):
        self._send("STATUS")

    def send_position(self):
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()
        if not x or not y:
            messagebox.showwarning("Fehlende Werte", "Bitte X und Y eingeben.")
            return
        self._send(f"POSITION {x} {y}")

    def send_stop(self):
        self._send("STOP")

    # ---------------- Log ----------------

    def _log(self, text: str):
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, text + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = UDPClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()