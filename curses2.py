#!/usr/bin/env python3
import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()

    begin_x = 20; begin_y = 7
    height = 5; width = 40
    win = curses.newwin(height, width, begin_y, begin_x)
    
    stdscr.addstr("Press 'p', 'UP arrow', or 'q' to quit.\n")
    stdscr.refresh()

    while True:
        c = stdscr.getch()
        
        if c == ord('p'):
            stdscr.addstr("\nYou pressed p")
        elif c == ord('q'):
            break
        elif c == curses.KEY_UP:
            stdscr.addstr("\nYou pressed the UP key")
        
        stdscr.refresh()
    
# Run
if __name__ == "__main__":
    wrapper(main)
