
import pickle
import socket
from _thread import *

import pygame

from models import Bullet, get_obstacles

W = 700
H = 400

player_connections = []

# Позиции для двух игроков
# Позиции для двух игроков
pos = [(350, 380), (350, 10)]  # Начальные координаты для каждого игрока
bullets = {0: [], 1: []}  # Словарь для хранения пуль каждого игрока
obstacles = get_obstacles()

player_one_count = player_two_count = 0

def check_game_over():
    global player_one_count, player_two_count
    if player_one_count >=5:

        popup_message = "Игрок 1 выиграл"
        player_one_count = player_two_count = 0
        return popup_message

    if player_two_count >=5:
        popup_message = "Игрок 2 выиграл"
        player_one_count = player_two_count = 0
        return popup_message

# Обновление пуль для каждого игрока
def update_bullets(player):
    global bullets
    other_player = 1 - player  # Получаем индекс другого игрока
    game_over = False  # Переменная для отслеживания окончания игры

    for bullet in bullets[player][:]:  # Итерируем по копии списка пуль текущего игрока
        bullet.move()

        # Проверяем столкновение пули с препятствиями
        if bullet.check_collision(obstacles):
            bullets[player].remove(bullet)
            continue

        # Проверяем попадание в другого игрока
        if bullet.rect.colliderect(pygame.Rect(*pos[other_player], 20, 10)):  # Проверяем столкновение с другим игроком
            print(f"Игрок {player} попал в игрока {other_player}!")
            bullets[player].remove(bullet)
            # Увеличиваем счет в зависимости от игрока
            if player == 0:
                global player_one_count
                player_one_count += 1
            else:
                global player_two_count
                player_two_count += 1

            game_over_message = ''
            # Проверяем конец игры
            game_over_message = check_game_over()
            if game_over_message:

                game_over = game_over_message  # Устанавливаем флаг окончания игры
            break

        # Удаляем пули, которые вышли за пределы экрана
        if bullet.x <= 0 or bullet.x >= (W - 100) or bullet.y <= 0 or bullet.y >= H:
            bullets[player].remove(bullet)

    return game_over  # Возвращаем состояние окончания игры

def threaded_client(conn, player):
    # Отправляем начальную позицию игрока
    conn.send(pickle.dumps(pos[player]))

    player_connections.append(conn)

    while True:
        try:
            # Получаем данные от клиента
            data = pickle.loads(conn.recv(4096))

            if not data:
                print("Disconnected")
                break

            if "position" in data:
                # Обновляем позицию игрока
                pos[player] = data["position"]
            # Обработка новых пуль
            elif "NEW_BULLET" in data:
                bullet_data = data["NEW_BULLET"]
                new_bullet = Bullet(**bullet_data)
                bullets[player].append(new_bullet)
                print("Полученные данные:", data)

            game_over = update_bullets(player)  # Проверяем обновление пуль и состояние игры

            # Формируем ответ для клиента
            reply = {}
            if game_over:

                reply["game_over"] = True  # Устанавливаем флаг окончания игры
                reply["message"] = "Конец игры!" + game_over # Сообщение о конце игры

                other_player_conn = player_connections[1 - player]  # Получаем соединение другого игрока
                if other_player_conn:
                    other_player_conn.sendall(pickle.dumps(reply))

            else:
                reply["position"] = pos[1 - player]  # Позиция другого игрока
                reply["bullets"] = [bullet.serialize() for bullet in bullets[player]] + \
                                   [bullet.serialize() for bullet in bullets[1 - player]]  # Пули обоих игроков
                reply["count"] = (player_one_count,player_two_count)
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
# s.bind(("0.0.0.0", 8000))
s.listen(2)

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
