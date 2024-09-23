import socket
from _thread import *
import sys


server = "192.168.0.107"
port = 8080


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)  # слушаем порт и ограничиваем кол-во поключенцев
print('Ожидайте подключения. Игра загружается')


pos = [(350, 380), (350,10)]   # стартовые позиции обиох игроков
pos_bullet = []

def read_pos(str):              # разбиваем получаемые координаты типа (67, 55) на две цифры
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())  # кол-во получаемых битов
            pos[player] = data

            if not data:                        # логирование сервера
                print('Дисконенктед')       # ксли нет данных
                break
            else:
                if player ==1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Получено:",data)          # пишем что получили и что вернули назад
                print("Отправлено:", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break



cur_player = 0
while True:
    conn, addr = s.accept()
    print(f'Соединяемся с:',addr)

    start_new_thread(threaded_client, (conn, cur_player))   # запускаем функцию отдльеным потоком через thread
    cur_player +=1 # при соединении добавляем игркоа в сипсок
