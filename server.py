import pickle
import socket
from _thread import *

# Позиции для двух игроков
pos = [(350, 380), (350, 10)]  # Начальные координаты для каждого игрока

def threaded_client(conn, player):
    # Отправляем начальную позицию игрока
    conn.send(pickle.dumps(pos[player]))

    while True:
        try:
            # Получаем данные от клиента
            data = pickle.loads(conn.recv(2048))
            print("data", data)
            pos[player] = data  # Обновляем позицию игрока

            if not data:
                print("Disconnected")
                break
            else:
                # Отправляем позицию другого игрока
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

# Серверная логика
currentPlayer = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8000))
s.listen(2)

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
