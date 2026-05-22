import socket
import threading
import json
import logging

HOST = 'localhost'
PORT = 3001

logging.basicConfig(
    filename="app_log_server.txt",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}

def handle_client(client_socket, client_address):
    try:
        # Отримуємо ім'я користувача при підключенні
        username = client_socket.recv(1024).decode('utf-8')
        clients[username] = client_socket
        print(f"Користувач {username} підключився")
        logging.info(f"Користувач {username} підключився")

        while True:
            # Очікуємо повідомлення
            header = client_socket.recv(4)
            if not header:
                break

            message_length = int.from_bytes(header, "big")
            data = b""
            while len(data) < message_length:
                packet = client_socket.recv(min(message_length - len(data), 4096))
                if not packet:
                    break
                data += packet
            message = json.loads(data.decode("utf-8"))
            recipient = message["Кому"]
            text = message["text"]
            FILE = message["file"]
            NAME = message["name"]
            
            # Пересилаємо повідомлення одержувачу
            if recipient in clients:
                formatted_msg = {"Від кого": username, "text": text, "file": FILE, "name": NAME}
                json_str = json.dumps(formatted_msg)
                message_bytes = json_str.encode("utf-8")
                header = len(message_bytes).to_bytes(4, byteorder="big")
                
                clients[recipient].sendall(header + message_bytes)
            else:
                client_socket.send(f"Помилка: Користувач {recipient} не знайдений.".encode('utf-8'))

    except ConnectionResetError:
        pass
    finally:
        # Видаляємо користувача при відключенні
        for name, sock in clients.items():
            if sock == client_socket:
                del clients[name]
                print(f"Користувач {name} відключився.")
                break
        client_socket.close()

def initial():
    print(f"Сервер запущено на {HOST}:{PORT}")
    while True:
        client_socket, client_address = server.accept()
        # Запускаємо окремий потік для кожного клієнта
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    initial()
