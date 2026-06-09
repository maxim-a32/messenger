import socket
import threading
import json
import base64
import os
import logging
import sqlite3

HOST = '127.0.0.1'
PORT = 3001

logging.basicConfig(
    filename="app_log_client.txt",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s")

# Функція для прийому повідомлень від сервера
def receive_messages(client_socket, conn, cursor):
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
            text = message['text'] + "\n"
            print(f"\n{message['Від кого']}:{message['text']}\n")
            logging.info("Прийшло повідомлення")
            cursor.execute('INSERT INTO messages (name, text) VALUES(?, ?)', (message['Від кого'], text))
            conn.commit()
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

def main(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            name TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    conn.commit()

    # Реєстрація на сервері
    #i = input("ведіть 1 щоб написати ім'я чи будьщо інше щоб було останне використане")
    if username != "":
        #username = input("Введіть ваше ім'я: ")
        client_name = {"name": username}
    else:
        try:
            with open("client_name.json", "r", encoding="utf-8") as file:
                client_name = json.load(file)
            username = client_name["name"]
        except:
            return 0, conn, client, cursor
    state = Connection(username, client, conn, cursor, client_name)
    return state, conn, client, cursor
        
def Connection(username, client, conn, cursor, client_name):
    client.send(username.encode('utf-8'))
    i = client.recv(1024).decode('utf-8')
    if i == "1":
        return 2
        #client.send(username.encode('utf-8'))
    else:
        with open("client_name.json", "w+", encoding="utf-8") as file:
            json.dump(client_name, file, ensure_ascii=False)

    # Запуск потоку для отримання повідомлень
    thread = threading.Thread(target=receive_messages, args=(client, conn, cursor,))
    thread.daemon = True
    thread.start()
    return 1

    #print("Для виходу натисніть Ctrl+C")
    #try:
    #    run = True
    #    while run:
    #        i = input("натисніть ентер щоб написати повідомлення обо ведіть 1 щоб переглянюти попередні повідомлення")
    #        if i == "1":
    #            history(conn, cursor)
    #        else:
    #            run = messeg(client, conn)
    #except KeyboardInterrupt:
    #    conn.close()
    #    client.close()
    # Створення і відправка повідомлень
def messeg(client, conn, user, text, file):
    try:
        if file:
            with open(file, "rb") as fille:
                binary_data = fille.read()
                encoded_string = base64.b64encode(binary_data).decode("utf-8")
            file_name, extension = os.path.splitext(file)
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
        return True
    except KeyboardInterrupt:
        client.close()
        conn.close()
        return False
def history(conn, cursor):
    try:
        cursor.execute("SELECT name, text FROM messages")
        rows = cursor.fetchall()
        data = ""
        for row in rows:
            i = f"Від кого: {row[0]} повідомлення: {row[1]}"
            data += i
        return data
    except:
        return "повідомлень немає"

if __name__ == "__main__":
    main()
