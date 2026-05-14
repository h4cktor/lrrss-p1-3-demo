import os
import base64
import json
import pickle

class Client:
    def __init__(self):
        self.user = None
        self.s_user = None
        self.opened_chat = None  # objeto Chat
        self.active_users = {}   # user: socket
        self.chats = {}          # user: objeto Chat
        self.messages = []
        self.global_messages = []

    def setClient(self, user, sock):
        if user is not None and sock is not None:
            self.user = user
            self.s_user = sock

    def createChat(self, user):
        self.chats[user] = Chat(user)

    def openChat(self, user):
        if user not in self.chats:
            self.createChat(user)

        self.opened_chat = self.chats[user]
        self.messages = self.opened_chat.messages
        
    def closeChat(self):
        self.opened_chat = None
        self.messages = []

    def addActiveUser(self, user, s_user=None):
        if user not in self.active_users:
            self.active_users[user] = s_user

    def delActiveUser(self, user):
        if user in self.active_users:
            self.active_users.pop(user)
            
    def manageMessages(self, mensajes):
        
        for mensaje in mensajes:
            if mensaje.get("type") == "fwd":
                sender = mensaje.get("from", "?")
                text = mensaje.get("msg", "")
                
                if sender not in self.chats:
                    self.createChat(sender)
                
                chat = self.chats[sender]   # Seleccionamos el chat del que envió el mensaje
                chat.messages.append(f"{sender}: {text}")
                # Bug fixed
                
                
            elif mensaje.get("type") == "file":
                sender = mensaje.get("from", "?")
                filename = mensaje.get("filename", "fichero_recibido")
                file_data = mensaje.get("data", "")

                os.makedirs("received_files", exist_ok=True)

                save_path = os.path.join(
                    "received_files",
                    f"{sender}_{filename}"
                )

                try:
                    with open(save_path, "wb") as f:
                        f.write(base64.b64decode(file_data.encode("utf-8")))

                    if sender not in self.chats:
                        self.createChat(sender)

                    chat = self.chats[sender]
                    chat.messages.append(f"{sender}: [fichero recibido] {save_path}")

                except Exception as e:
                    if sender not in self.chats:
                        self.createChat(sender)

                    chat = self.chats[sender]
                    chat.messages.append(f"[error recibiendo fichero de {sender}] {e}")               
                
                

            elif mensaje.get("type") in ("online", "offline", "login_ok"):
                pass

            elif mensaje.get("type") == "active_users":
                self.active_users = json.loads(mensaje.get("users"))
                
                for user in self.active_users:  # Creamos los chats si no están creados ya
                    if user is not self.user and user not in self.chats:
                        self.createChat(user)        

            elif mensaje.get("type") == "disc_user":    # "user": "{"br1": ["127.0.0.1", 49868]}"
                user = mensaje.get("user")
                self.delActiveUser(user)
            
            elif mensaje.get("type") == "new_user":
                
                res = json.loads(mensaje.get("user"))   # "{"br1": ["127.0.0.1", 49868]}"
                user = next(iter(res))    
                s_user = res[user]
                self.addActiveUser(user, s_user)
                
                if user not in self.chats:
                    self.createChat(user)
         
    def saveClient(self): # Solo guardamos los mensajes, que es lo interesante
                          # De hecho los sockets no los podríamos serializar

        data_to_save =  self.chats
        
        with open(f"{self.user}.pickle", 'wb') as f:
            pickle.dump(data_to_save, f, pickle.HIGHEST_PROTOCOL)
        
    def loadClient(self, user, sock): # clase generada con s_user
        with open(f"{user}.pickle", 'rb') as f:
            self.chats = pickle.load(f)   # Igual se podría pensar en encriptar  
        self.user = user
        self.s_user = sock
            

class Chat:
    def __init__(self, to):
        self.to = to
        self.messages = []
        