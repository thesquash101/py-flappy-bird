import curses
import sys

# Set terminal type
stdscr = curses.initscr()

# Turns off echoing keys
curses.noecho()

# Keys react instantly
curses.cbreak()

# Special keys
stdscr.keypad(True)

# Terminate old proc
curses.nocbreak()
stdscr.keypad(False)
curses.echo()

# Restore terminal to non-curses
# curses.endwin()

from curses import wrapper

def main(stdscr):
    stdscr.clear()

begin_x = 20; begin_y = 7
height = 5; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
stdscr.refresh()
stdscr.getkey()

curses.echo()

while True:
    c = stdscr.getch()
    if c == ord('p'):
        stdscr.addstr("you pressed p")
    elif c == ord('q'):
        break
    elif c == curses.KEY_UP:
        stdscr.addstr("pressed pey")

curses.echo()

s = stdscr.getstr(0,0, 15)

wrapper(main)
