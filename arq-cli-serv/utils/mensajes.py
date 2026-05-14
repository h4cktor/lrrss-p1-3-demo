import json
import pdb


def parse_msg(sock, msg_type, *argv, verbose=False):
    msg = {"type": msg_type}

    if msg_type in ("login", "disc_user"):
        msg["user"] = argv[0]
        
    elif msg_type in ("login_ok", "offline", "online", "search_active"):
        pass

    elif msg_type == "active_users":
        users = {}
        for user, sock in argv[0].items():
            users[user] = sock.getpeername()
        
        res = json.dumps(users)
        msg["users"] = res
            
    elif msg_type == "new_user":
        user = {}
        user[argv[0]] = argv[1].getpeername()
        
        res = json.dumps(user)
        msg["user"] = res

    elif msg_type == "send":
        msg["to"] = argv[0]
        msg["msg"] = argv[1]

    elif msg_type == "fwd":
        msg["from"] = argv[0]
        msg["msg"] = argv[1]

    elif msg_type == "broadcast":
        msg["msg"] = argv[0]

    elif msg_type == "send_file":
        msg["to"] = argv[0]
        msg["filename"] = argv[1]
        msg["data"] = argv[2]

    elif msg_type == "file":
        msg["from"] = argv[0]
        msg["filename"] = argv[1]
        msg["data"] = argv[2]

    else:
        return

    mensaje = json.dumps(msg)
    return mensaje
    

def send_msg(sock, msg_type, *argv, verbose=False):
    parsed_msg = parse_msg(sock, msg_type, *argv, verbose)
    
    if verbose:
        print("\n[SERVIDOR]: ")
        print(parsed_msg)
        print()

    sock.sendall(parsed_msg.encode())
      

def get_msg(data):

    msg_list = []
    buff = data.decode()
    mensajes = buff.replace('}{', '} | {').split(' | ')
    for mensaje in mensajes:
        mensaje_json = json.loads(mensaje)
        msg_list.append(mensaje_json) 
        
    return msg_list


