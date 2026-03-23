#!/usr/bin/env python3
import curses
from curses import wrapper
import random
import time

running = True
score = 0
charPositionX = 10; 
charPositionY = 5; 

# Pipe variables
pipeWidth = 4
pipeGap = 8
pipeSpeed = 1
pipeRand = []

def main(stdscr):
    curses.curs_set(0)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def drawBird():
        """Draw the bird"""
        try:
            stdscr.addch(charPositionY, charPositionX, 'O', curses.color_pair(1) | curses.A_BOLD)
        except curses.error:
            pass  # Ignore if out of bounds

    def drawPipe(self):
        for pipe in self.pipes:
            pipe_x = pipeRand['x']

            # Top pipe // Review code (AI)
            for y in range(pipe['top_height']):
                try:
                    self.stdscr.addch(y, pipe_x, '|', curses.color_pair(2))
                    self.stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(2))
                except curses.error:
                    pass

            # Bottom pipe // review
            for y in range(pipe['bottom_start'], self.height - 1):
                try:
                    self.stdscr.addch(y, pipe_x, '|', curses.color_pair(2))
                    self.stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(2))
                except curses.error:
                    pass
                
    def checkBounds():
        if (charPositionY == 0 or charPositionY == 10):
            gameEnd()

    def gameEnd():
        stdscr.addstr("Game Over\n")
        stdscr.addstr("Your score was: " + score)
        stdscr.addstr("Press q to exit...")

        quit = stdscr.getch()
        
        # Call global from top
        global running

        if quit == ord('q'):
            running = False
        elif quit == ord('q'):
            stdscr.addstr("Press q to exit...")
        

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