import curses
from utils import mensajes as msg

def manage_input(ch, client, current_input):   

    if ch in (10, 13):  # Enter
        text = current_input.strip()

        if text == "exit":
            client.closeChat()

        elif text:
            if client.opened_chat == None:
                client.openChat(text)
                
            else:    
                msg.send_msg(client.s_user, "send", client.opened_chat.to, text)
                client.messages.append(f"yo: {text}")

        current_input = ""

    elif ch in (127, 8, curses.KEY_BACKSPACE): # Borrar
        current_input = current_input[:-1]

    elif 32 <= ch <= 126:
        current_input += chr(ch)
        
    return current_input

            