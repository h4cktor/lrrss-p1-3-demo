import sys
import socket
import select
import argparse
import signal

from curses import wrapper

from utils import mensajes as msg
from client_app.classes import Client
from client_app.ui import init_ui, draw
from client_app.handlers import manage_input


def signal_handler(signal, frame, client):
    try:
        client.saveClient()
        sys.exit(0)
    except Exception as e:
        print(e)
        print("\nError guardando chats")
        sys.exit(1)


def set_parser():
    
    parser = argparse.ArgumentParser(
        prog="client",
        description="Cliente de python de mensajería modelo cliente-servidor"
    )

    parser.add_argument('-i', '--ip', default="127.0.0.1")
    parser.add_argument('-p', '--port', type=int, default=8080)
    parser.add_argument('-u', '--user', type=str)
    return parser.parse_args()    

def app(stdscr, client):
    msg_win, input_win, users_win = init_ui(stdscr)

    current_input = ""

    while True:
        draw(msg_win, input_win, users_win, current_input, client)

        rdy_read, _, _ = select.select([client.s_user], [], [], 0.05)

        for ready in rdy_read:
            if ready == client.s_user:
                data = client.s_user.recv(65535)

                if not data:
                    return

                mensajes = msg.get_msg(data)
                client.manageMessages(mensajes)
                
        ch = stdscr.getch()
        if ch == -1:
            continue
        
        current_input = manage_input(ch, client, current_input)


def main():

    args = set_parser()
    
    client = Client()

    signal.signal(signal.SIGINT, lambda s,f: signal_handler(s,f,client))

    if not args.user:
        user = input("Introduce tu usuario: ")
    else:
        user = args.user

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.connect((args.ip, args.port))
        except ConnectionRefusedError:
            print("Conexión rechazada, está el servidor activo?")
            return

        try:
            client.loadClient(user, s)

        except:
            print(f"\nNo existen mensajes para {user}")
            client.setClient(user, s)
        
        msg.send_msg(client.s_user, "login", user)
        msg.send_msg(client.s_user, "search_active")

        # Hay que llamarlo así porque wrapper solo recibe 1 argumento
        def run(stdscr):
            app(stdscr, client)

        wrapper(run)


if __name__ == "__main__":
    main()
    