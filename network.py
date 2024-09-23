import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 8000
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            # Получаем начальные данные от сервера (используем pickle)
            return pickle.loads(self.client.recv(2048))  # Получаем данные как байты и декодируем с помощью pickle
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            # Отправляем данные в виде байтов, сериализованных с помощью pickle
            self.client.send(pickle.dumps(data))
            # Получаем ответ от сервера (также в байтовом формате)
            return pickle.loads(self.client.recv(2048))  # Декодируем полученные данные с помощью pickle
        except socket.error as e:
            print(e)