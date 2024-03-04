import sys
import time
import socket
import select

from src.helpers import get_list_ip, remove_ip_list

delay = 0.0001
delay_reconnect = 1
buffer_size = 4096


class _Forward:
    def __init__(self):
        self.host = None
        self.port = None
        self.forward = None
        self.connected = False

    def connect(self, host, port, timeout):
        self.host = host
        self.port = port
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.forward.settimeout(timeout)
        try:
            self.forward.connect((host, port))
            self.connected = True
            return self.forward
        except socket.timeout:
            self.forward.close()
            self.connected = False
            remove_ip_list(host, port)
            return self.reconnect(timeout)
        except Exception as e:
            self.connected = False
            print("Error connecting to forward:", e)
            raise

    def reconnect(self, timeout):
        while not self.connected:
            time.sleep(delay_reconnect)
            try:
                host, port = get_list_ip()
                print("Attempting to reconnect to forward:", host, port)
                self.connect(host, int(port), timeout)
                print("Reconnected to forward:", host, port)
                self.connected = True
                break
            except Exception as e:
                print("Reconnection attempt failed:", e)
                time.sleep(1)
                continue
        return self.forward


class _Proxy:
    input_list = []
    channel = {}

    def __init__(self, host, port, ipForward, portFoward, timeout):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)
        self.proxyForwardIp = ipForward
        self.proxyForwardPort = portFoward
        self.timeout = timeout

    def main_loop(self):
        self.input_list.append(self.server)

        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                try:
                    self.data = self.s.recv(buffer_size)
                    if len(self.data) == 0:
                        self.on_close()
                        break
                    else:
                        self.on_recv()

                except Exception as e:
                    print(e)
                    self.on_close()
                    break

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        forward = _Forward().connect(self.proxyForwardIp, self.proxyForwardPort, self.timeout)
        if forward:
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
    def on_close(self):
        try:
            print(self.s.getpeername(), "disconnected")
        except Exception as e:
            print(e)
            print("Client closed")

        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()  # equivalent to do self.s.close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]


    def on_recv(self):
        data = self.data
        self.channel[self.s].send(data)



def proxy_forward(proxyPort, proxyBinding, timeout):
    host, port = get_list_ip()
    proxy = _Proxy(proxyBinding, proxyPort, host, int(port), int(timeout))
    proxy.main_loop()

    
