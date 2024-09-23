import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.107"
        self.port = 8080
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):      # метод подключения
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()   # после подключения мы сразу получаем ответную инфу от серввера

        except:
            pass


    def send (self, data):     # метод отправки сообщений
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()

        except socket.error as e:
            print(str(e))

