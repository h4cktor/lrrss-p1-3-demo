import sys
import argparse
import signal

from curses import wrapper

from utils import mensajes as msg
from client_app.classes import Client
from client_app.ui import init_ui, draw
from client_app.handlers import manage_input
from client_app.ws_adapter import WebSocketAdapter


def signal_handler(signal, frame, client):
    try:
        client.saveClient()
        if client.s_user is not None:
            client.s_user.close()
        sys.exit(0)
    except Exception as e:
        print(e)
        print("\nError guardando chats")
        sys.exit(1)


def set_parser():
    parser = argparse.ArgumentParser(
        prog="client",
        description="Cliente de python de mensajería usando AWS WebSocket API"
    )

    parser.add_argument(
        '-u',
        '--url',
        default="wss://b2k0zw5ca5.execute-api.us-east-1.amazonaws.com/dev",
        help="URL WebSocket de API Gateway"
    )

    parser.add_argument(
        '--user',
        type=str,
        help="Nombre de usuario"
    )

    return parser.parse_args()


def app(stdscr, client):
    msg_win, input_win, users_win = init_ui(stdscr)

    current_input = ""

    while True:
        draw(msg_win, input_win, users_win, current_input, client)

        try:
            data = client.s_user.recv_nonblocking()
        except Exception:
            data = None

        if data:
            mensajes = msg.get_msg(data)
            client.manageMessages(mensajes)

        ch = stdscr.getch()
        if ch == -1:
            continue

        current_input = manage_input(ch, client, current_input)


def main():
    args = set_parser()

    client = Client()

    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, client))

    if not args.user:
        user = input("Introduce tu usuario: ")
    else:
        user = args.user

    try:
        s = WebSocketAdapter(args.url)
    except Exception as e:
        print(f"No se pudo conectar al WebSocket: {e}")
        return

    try:
        client.loadClient(user, s)
    except Exception:
        print(f"\nNo existen mensajes para {user}")
        client.setClient(user, s)

    msg.send_msg(client.s_user, "login", user)
    msg.send_msg(client.s_user, "search_active")

    def run(stdscr):
        app(stdscr, client)

    wrapper(run)


if __name__ == "__main__":
    main()
    