import socket
import threading
import json
import base64
import os
import logging

HOST = '127.0.0.1'
PORT = 3001

logging.basicConfig(
    filename="app_log_client.txt",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s")

# Функція для прийому повідомлень від сервера
def receive_messages(client_socket):
    while True:
        try:
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
            print(f"\n{message['Від кого']}:{message['text']}\n")
            logging.info("Прийшло повідомлення")
            histori = f"\n{message['Від кого']}:{message['text']}\n"
            with open("chat history.txt", "a+", encoding="utf-8") as file:
                file.write(histori)
            try:
                decoded_data = base64.b64decode(message["file"])
                output_path = message["name"]
                with open(output_path, "wb") as filee:
                    filee.write(decoded_data)
                print(f"фаїл який прийшов збережено під назвою {output_path}\n")
            except:
                pass
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Реєстрація на сервері
    username = input("Введіть ваше ім'я: ")
    client.send(username.encode('utf-8'))

    # Запуск потоку для отримання повідомлень
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    print("Для виходу натисніть Ctrl+C")

    # Створення і відправка повідомлень
    try:
        while True:
            i = input("натисніть ентер щоб написати повідомлення обо ведіть 1 щоб переглянюти попередні повідомлення")
            if i == "1":
                try:
                    with open("chat history.txt", "r", encoding="utf-8") as File:
                        textt = File.read()
                        print(textt)
                except:
                    print("повідомлень немає")
            else:
                user = input("ведіть отримувача")
                text = input("ведіть текст повдомлення")
                filee = input("якщо бажаєте відправити фаїл то натисніть 1 якщо ні то будьщо інше")
                if filee == "1":
                    file = input("скопіюйте і вставте повний шлях до файла який бажаєте відправити")
                    with open(file, "rb") as fille:
                        binary_data = fille.read()
                        encoded_string = base64.b64encode(binary_data).decode("utf-8")
                    file_name, extension = os.path.splitext(file)
                    print(file_name)
                    filee_name = os.path.basename(file_name)
                    FILE = filee_name + extension
                else:
                    encoded_string = None
                    FILE = None
                
                messagee = {"Кому": user, "text": text, "file": encoded_string, "name": FILE}
                json_str = json.dumps(messagee)
                message_bytes = json_str.encode("utf-8")
                header = len(message_bytes).to_bytes(4, byteorder="big")
                client.sendall(header + message_bytes)
                logging.info("Повідомлення відправлено")
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    main()
