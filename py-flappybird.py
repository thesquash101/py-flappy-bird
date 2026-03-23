#!/usr/bin/env python3
import curses
from curses import wrapper
import random
import time

running = True
score = 0
charPositionX = 10; 
charPositionY = 5; 

def main(stdscr):
    curses.cursSet(0)
    
    curses.startColor()
    curses.initPair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def drawBird():
        """Draw the bird"""
        try:
            stdscr.addch(charPositionY, charPositionX, 'O', curses.color_pair(1) | curses.A_BOLD)
        except curses.error:
            pass  # Ignore if out of bounds

    def checkBounds():
        if (charPositionY == 0 or charPositionY == 10):
            gameEnd()

    def gameEnd():
        

    while running:
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.refresh()

        drawBird()

        c = stdscr.getch()
        
        if c == ord('q'):
            break
        elif c == curses.KEY_UP or ord(' '):
            stdscr.addstr("\nJUMP")
        stdscr.refresh()

        # Game speed
        time.sleep(0.2)
    
# Run
if __name__ == "__main__":
    wrapper(main)