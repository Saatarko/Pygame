
import pickle
import socket
from _thread import *

from models import Bullet

# Позиции для двух игроков
pos = [(350, 380), (350, 10)]  # Начальные координаты для каждого игрока

bullets = {0: [], 1: []}  # Словарь для хранения пуль каждого игрока

def threaded_client(conn, player):
    # Отправляем начальную позицию игрока
    conn.send(pickle.dumps(pos[player]))

    while True:
        try:
            # Получаем данные от клиента
            data = pickle.loads(conn.recv(2048))
            print("data", data)

            # Обновляем позицию игрока
            pos[player] = data["position"]  # Обновляем позицию игрока

            if not data:
                print("Disconnected")
                break

            if "NEW_BULLET" in data:
                bullet_data = data["NEW_BULLET"]
                bullet = Bullet(**bullet_data)  # Создаем пулю и добавляем в соответствующий список
                bullets[player].append(bullet)

            # Подготовка ответа для клиента
            reply = {
                "position": pos[1 - player],  # Позиция другого игрока
                "bullets": [bullet.__dict__ for bullet in bullets[1 - player]]  # Пули другого игрока
            }

            print("Sending:", reply)
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print(f"Error: {e}")
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
