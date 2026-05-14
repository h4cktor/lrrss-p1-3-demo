import json
import pdb


def send_msg(sock, msg_type, *argv, verbose=False):
    msg = {
        "type": msg_type,
        "action": msg_type
    }

    if msg_type == "login":
        msg["user"] = argv[0]

    elif msg_type == "search_active":
        pass

    elif msg_type in ("login_ok", "offline", "online"):
        pass

    elif msg_type == "active_users":
        users = {}

        for user, sock_user in argv[0].items():
            try:
                users[user] = sock_user.getpeername()
            except Exception:
                users[user] = None

        res = json.dumps(users)
        msg["users"] = res

    elif msg_type == "new_user":
        user = {}

        try:
            user[argv[0]] = argv[1].getpeername()
        except Exception:
            user[argv[0]] = None

        res = json.dumps(user)
        msg["user"] = res

    elif msg_type == "disc_user":
        msg["user"] = argv[0]

    elif msg_type == "send":
        msg["action"] = "sendmessage"
        msg["to"] = argv[0]
        msg["msg"] = argv[1]

    elif msg_type == "fwd":
        msg["from"] = argv[0]
        msg["msg"] = argv[1]

    else:
        return

    mensaje = json.dumps(msg)

    if msg_type not in ("login", "send") and verbose:
        print("\n[SERVIDOR]: ")
        print(mensaje)
        print()

    sock.sendall(mensaje.encode())


def get_msg(data):
    msg_list = []

    if isinstance(data, bytes):
        buff = data.decode()
    else:
        buff = data

    mensajes = buff.replace('}{', '} | {').split(' | ')

    for mensaje in mensajes:
        if mensaje.strip():
            mensaje_json = json.loads(mensaje)
            msg_list.append(mensaje_json)

    return msg_list
