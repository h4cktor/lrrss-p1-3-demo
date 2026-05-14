import websocket


class WebSocketAdapter:
    def __init__(self, url):
        self.url = url
        self.ws = websocket.create_connection(url)
        self.ws.settimeout(0.05)

    def sendall(self, data):
        if isinstance(data, bytes):
            data = data.decode()
        self.ws.send(data)

    def recv(self, size=65535):
        data = self.ws.recv()

        if data is None:
            return b""

        if isinstance(data, bytes):
            return data

        return data.encode()

    def recv_nonblocking(self):
        try:
            return self.recv(65535)
        except websocket.WebSocketTimeoutException:
            return None

    def close(self):
        self.ws.close()
        