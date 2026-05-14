import curses

USERS_WIDTH = 20
INPUT_HEIGHT = 3

def init_ui(stdscr):
    curses.curs_set(1)
    curses.noecho()
    stdscr.nodelay(True)

    max_y, max_x = stdscr.getmaxyx()

    users_win = curses.newwin(max_y - INPUT_HEIGHT, USERS_WIDTH, 0, 0)
    msg_win = curses.newwin(max_y - INPUT_HEIGHT, max_x - USERS_WIDTH, 0, USERS_WIDTH)
    input_win = curses.newwin(INPUT_HEIGHT, max_x, max_y - INPUT_HEIGHT, 0)

    return msg_win, input_win, users_win


def draw(msg_win, input_win, users_win, current_input, client):
    msg_win.erase()
    input_win.erase()
    users_win.erase()
    
    msg_win.box()
    input_win.box()
    users_win.box()

    # Representación de usuarios activos
    users_win.addstr(1,1, "Usuarios activos", curses.A_UNDERLINE)
    fila = 3
    for user in client.active_users.keys():
        if user != client.user: 
            if client.opened_chat is not None and user == client.opened_chat.to:
                users_win.addstr(fila,1, f"{user}", curses.A_REVERSE)
            else:
                users_win.addstr(fila,1, f"{user}")
            fila += 1
    
    if client.opened_chat == None:
        msg_win.addstr(1,1, "Escribe a que usuario deseas contactar")
        input_win.addstr(1,1, f"[Destino] {current_input}")
        
    else:        
        y = 1
        for line in client.messages:
            msg_win.addstr(y, 1, line)
            y += 1

        input_win.addstr(1, 1, f"[{client.user}>{client.opened_chat.to}] {current_input}")

    msg_win.noutrefresh()
    users_win.noutrefresh()
    input_win.noutrefresh()
    curses.doupdate()
    