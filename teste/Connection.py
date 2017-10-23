import socket
import threading

class Server(threading.Thread):
    host = "127.0.0.1"
    port = 5000
    nome = ""
    mySocket = socket.socket()

    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        mySocket = socket.socket()
        mySocket.bind((self.host, self.port))

        mySocket.listen(1)
        conn, addr = mySocket.accept()
        print("Recive connection from: " + str(addr))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("from connected  user: " + str(data))

            data = str(data).upper()
            print("sending: " + str(data))
            conn.send(data.encode())
        conn.close()


class  Client(threading.Thread):
    host = '127.0.0.1'
    port = 5000
    nome = ""
    mySocket = socket.socket()

    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        mySocket = socket.socket()
        mySocket.connect((self.host, self.port))

        message = input(" -> ")

        while message != 'q':
            mySocket.send(message.encode())
            data = mySocket.recv(1024).decode()

            print('Received from server: ' + data)

            message = input(" -> ")

        mySocket.close()

s = Server("Servidor")
c = Client("Cliente")

s.start()
c.start()

l = []
l.append(s)
l.append(c)

for t in l:
    t.join()
