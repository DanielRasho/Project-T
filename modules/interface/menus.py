from readchar import readkey, key  
import os

    
def menu_builder(header: str, options: list, footer: str, return_value = False, default_options = []):
    cursor_position = 0
    options += default_options

    while True:
        
        clean_screen()
        print(f"{header}\n")
        for index, option in enumerate(options):
            if index == cursor_position:
                print(f"\t>> {option}")
            else:
                print(f"\t   {option}")
        print(f"\n{footer}")

        
        new_cursor_position = readkey()
        if new_cursor_position == key.UP:         
            cursor_position -= 1
            cursor_position %= len(options)
        elif new_cursor_position == key.DOWN:     
            cursor_position += 1
            cursor_position %= len(options)
        elif new_cursor_position == key.ENTER:   
            if return_value is True: return options[cursor_position]
            else: return cursor_position

def clean_screen():
    # Cleans terminal screen  
    if os.name == "posix":  # If program is executed in Linux or Mac
        os.system("clear")
    else:
        os.system("cls")