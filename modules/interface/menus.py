import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from typing import List

def print_centered(window: curses.window, text:str, optional_message:str = ""):
    height = text.count("\n")
    width = 0
    for row in text.split("\n"):
        if len(row) > width:
            width = len(row)
    y, x = window.getmaxyx()
    y_banner = y//2 - height//2
    x_banner = x//2 - width//2
    window.clear()
    
    rectangle(window, y_banner, x_banner-2, y_banner+height, x_banner+width+2)
    window.addstr(y_banner-2, x//2-len(optional_message)//2, optional_message)
    for row in text.split("\n"):
        window.addstr(y_banner, x_banner, row)
        y_banner += 1
    window.refresh()

def centered_coords(window: curses.window, width: int, height: int):
    h, w = window.getmaxyx()
    x = w // 2 - width // 2
    y = h // 2 - height // 2
    return (x, y)

def centered_box(window: curses.window, width: int, height: int):
    x, y = centered_coords(window, width, height)
    box = curses.newwin(height, width, y, x)
    rectangle(window, y - 1, x - 1, y + height, x + width)
    window.refresh()
    return box

def textbox_builder(
    window: curses.window, width: int, height: int, header: str, footer: str
) -> str:
    # BOXES CREATION
    box = centered_box(window, width, height)
    x_cord, y_cord = centered_coords(window, width, height)
    h, w = box.getmaxyx()
    sub_box = curses.newwin(1, width - 4, y_cord + height - 5, x_cord + 2)
    textbox = Textbox(sub_box)

    # DRAWING BOXES
    rectangle(box, height - 6, 1, height - 4, width - 2)
    box.addstr(0, w // 2 - len(header) // 2, header, curses.A_UNDERLINE)
    box.addstr(h - 2, w // 2 - len(footer) // 2, footer, curses.color_pair(2))

    # GETTING USER INPUT
    box.refresh()
    sub_box.refresh()
    curses.curs_set(1)
    textbox.edit()
    curses.curs_set(0)
    # CLEARING OUT
    window.clear()

    return textbox.gather().replace(" ", "")

def alert_message(window: curses.window, width, height, title, content, ending):
    box = centered_box(window, width, height)
    y, x = box.getmaxyx()
    # ADDING THE CONTENT TO THE BOX
    box.addstr(0, x // 2 - len(title) // 2, title, curses.A_UNDERLINE)
    box.addstr(2, 0, content)
    box.addstr(y - 1, x // 2 - len(ending) // 2, ending, curses.color_pair(2))
    box.refresh()
    # ERASING THE ALERT_MESSAGE IF ENTER KEY IS PRESSED
    while True:
        key = box.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            box.clear()
            window.clear()
            box.refresh()
            del box
            break

def menu_builder(
    window: curses.window,
    width: int,
    header: str,
    options: List[str],
    footer: str,
    default_options: List[str] = [],
) -> str:
    options += default_options
    height = len(options) + 5
    box = centered_box(window, width, height)
    selected_row = 0
    while True:
        # DRAW MENU
        box.clear()
        box.addstr(0, width // 2 - len(header) // 2, header, curses.A_UNDERLINE)
        for row, value in enumerate(options, ):
            if row == selected_row:
                box.addstr(row+2, width // 2 - len(value) // 2, value, curses.color_pair(2))
            else:
                box.addstr(row+2, width // 2 - len(value) // 2, value)
        box.addstr(height - 1, width // 2 - len(footer) // 2, footer)
        box.refresh()

        # CHANGE ROW
        key = window.getch()
        if key == curses.KEY_UP:         
            selected_row -= 1
            selected_row %= len(options)
        elif key == curses.KEY_DOWN:     
            selected_row += 1
            selected_row %= len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:   
            window.clear()
            return options[selected_row]

def confirmation_box(window: curses.window, message:str) -> bool:
    window.clear()
    answer = menu_builder(window, 50, message, ["SI", "NO"], footer="Presiona <Enter> para confirmar.")
    if answer == "SI":
        return True
    if answer == "NO":
        return False


def es_telefono_valido(telefono:str):
    validacion = telefono.replace("\n", "").strip().isnumeric()
    if validacion==False:
        return False
    elif len(telefono) != 8:
        return False
    else:
        return True
