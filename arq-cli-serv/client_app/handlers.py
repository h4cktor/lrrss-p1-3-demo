import os
import base64
import curses
from utils import mensajes as msg

def manage_input(ch, client, current_input):   

    if ch in (10, 13):  # Enter
        text = current_input.strip()

        if text == "/exit":
            client.closeChat()
            current_input = ""

        elif text.startswith("@all"):
            parts = text.split("@all")
            msg.send_msg(client.s_user, "broadcast", parts[1].strip()) 
            client.global_messages.append(f"yo->@all {parts[1].strip()}")
            current_input = ""

        elif text:
            if client.opened_chat == None:
                client.openChat(text)
                current_input = ""
                
            else:
                if text.startswith("/file "):
                    filepath = text.split("/file ", 1)[1].strip()

                    if os.path.getsize(filepath) > 2 * 1024: # Son 2KB
                        client.messages.append("[error] El fichero es demasiado grande. Máximo: 2 KB")
                    else:
                        with open(filepath, "rb") as f:
                            data = base64.b64encode(f.read()).decode("utf-8")

                        filename = os.path.basename(filepath)

                        msg.send_msg(client.s_user, "send_file", client.opened_chat.to, filename, data)
                        client.messages.append(f"yo: [fichero enviado] {filename}")

                    current_input = ""
                        
                else:
                    msg.send_msg(client.s_user, "send", client.opened_chat.to, text)
                    client.messages.append(f"yo: {text}") 
                    current_input = ""

    elif ch in (127, 8, curses.KEY_BACKSPACE): # Borrar
        current_input = current_input[:-1]

    elif 32 <= ch <= 126:
        current_input += chr(ch)
        
    return current_input

            