import curses
import subprocess
import os
import time

def main():
    showInitMessage()
    try:
        subprocess.run(["/bin/python3", "bin/pysh.py"])
    except:
        curses.wrapper(logonMenu)

def showInitMessage(path="/etc/pysh_wmsg"):
    with open(path, "r") as f:
        welcomeMsg = f.read().splitlines()
        f.close()
    for line in welcomeMsg:
        if line.strip().startswith("#"):
            continue
        print(line)

def drawMenu(stdscr, menu, selected, title, additionalTitle=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    titleMsg = ((w - len(title)) // 2) * " " + title + ((w - len(title)) // 2) * " "
    stdscr.addstr(0, 0, titleMsg)
    stdscr.addstr(0, (w - len(title)) // 2, title)
    for idx, item in enumerate(menu):
        x = (w - len(item)) // 2
        y = 2 + idx

        if idx == selected:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, item)
        
    if additionalTitle:
        stdscr.addstr(4 + len(menu), (w - len(additionalTitle)) // 2, additionalTitle)
    stdscr.refresh()

def logonMenu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.cbreak()
    stdscr.keypad(True)

    menu = [
        "LOGON", 
        "REBOOT", 
        "POWER OFF",
        "HALT SYSTEM"
    ]

    title = "PythOS LOGON MENU"
    selected = 0 

    drawMenu(stdscr=stdscr, title=title, menu=menu, selected=selected)
    while True:
        additionalTitle = ""
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            if selected == 0:
                selected = len(menu)
            else:
                selected -= 1
        elif key == curses.KEY_DOWN:
            if selected == len(menu):
                selected = 0
            else:
                selected += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            if menu[selected] == "LOGON":
                subprocess.run(["/bin/python3", "/bin/pysh.py"])
            elif menu[selected] == "POWER OFF":
                additionalTitle = "The system will shutdown NOW!"
                time.sleep(2)
                subprocess.run(["/bin/shutdown"])
            elif menu[selected] == "REBOOT":
                additionalTitle = "The system will reboot NOW!"
                subprocess.run(["/bin/reboot"])
            elif menu[selected] == "HALT SYSTEM":
                additionalTitle = "The system will halt NOW!"
                subprocess.run(["/bin/halt"])
