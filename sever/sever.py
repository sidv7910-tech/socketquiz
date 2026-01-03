import socket
import threading

HOST = '0.0.0.0'
PORT = 9999

scores = {}

questions = [
    ("99 + 900 = ?", "999"),
    ("Ngay Bac Ho doc ban tuyen ngon doc lap:", "2 thang 9 nam 1945"),
    ("Oxi hoa Dong tao ra gi:", "oxit cua dong")
]

def handle_client(conn, addr):
    print(f"[NEW] {addr} connected")

    conn.send("Nhap ten cua ban: ".encode())
    name = conn.recv(1024).decode().strip()
    scores[name] = 0

    for q, ans in questions:
        conn.send(f"\nCau hoi: {q}\nTra loi: ".encode())
        reply = conn.recv(1024).decode().strip()

        if reply.lower() == ans.lower():
            scores[name] += 1
            conn.send("Dung roi!\n".encode())
        else:
            conn.send(f"Sai roi! Dap an dung la: {ans}\n".encode())

    result = "\nKet qua cuoi cung:\n"
    for k, v in scores.items():
        result += f"{k}: {v} diem\n"

    conn.send(result.encode())
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER] Dang chay...")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr)
        ).start()

start_server()
