#!/usr/bin/env python3
import curses
from curses import wrapper
import random
import time

running = True
score = 0
charPositionY = 10; 


def main(stdscr):
    while running:
        stdscr.clear()

        c = stdscr.getch()
        
        if c == ord('p'):
            stdscr.addstr("\nYou pressed p")
        elif c == ord('q'):
            break
        elif c == curses.KEY_UP or ord(' '):
            stdscr.addstr("\nYou pressed the UP key")
        stdscr.refresh()

        # Game speed
        time.sleep(0.1)
    
# Run
if __name__ == "__main__":
    wrapper(main)