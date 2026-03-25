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
pipes = []

def main(stdscr):
    height, width = stdscr.getmaxyx()
    global pipes, score
    curses.curs_set(0)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def drawBird():
        """Draw the bird"""
        try:
            stdscr.addch(charPositionY, charPositionX, 'O', curses.color_pair(1) | curses.A_BOLD)
        except curses.error:
            pass  # Ignore if out of bounds

    def drawPipe():
        for pipe in pipes:
            pipe_x = pipe['x']

            # Top pipe // Review code (AI)
            for y in range(pipe['top_height']):
                try:
                    stdscr.addch(y, pipe_x, '|', curses.color_pair(1))
                    stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(1))
                except curses.error:
                    pass

            # Bottom pipe // review
            for y in range(pipe['bottom_start'], height - 1):
                try:
                    stdscr.addch(y, pipe_x, '|', curses.color_pair(1))
                    stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(1))
                except curses.error:
                    pass

    def updatePipe():
        global score
        # Move pipes
        for pipe in pipes[:]:
            pipe['x'] -= pipeSpeed
            if pipe['x'] + pipeWidth < 0:
                pipes.remove(pipe)
                score += 1

        height, width = stdscr.getmaxyx()

        if not pipes or pipes[-1]['x'] < width - 20:
            top_height = random.randint(2, height - pipeGap - 2)
            bottom_start = top_height + pipeGap
            pipes.append({
                'x': width - 1,
                'top_height': top_height,
                'bottom_start': bottom_start
            })

    def checkBounds():
        if (charPositionY == 0 or charPositionY == 10):
            gameEnd()

    def gameEnd():
        global score, running

        stdscr.nodelay(False)  # 👈 THIS is the key fix

        stdscr.clear()

        stdscr.addstr(5, 5, "Game Over")
        stdscr.addstr(6, 5, "Your score was: " + str(score))
        stdscr.addstr(7, 5, "Press any key to exit...")

        stdscr.refresh()
        stdscr.getch()  # now this will actually wait

        running = False

    while running:
        stdscr.nodelay(True)
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.refresh()
        global charPositionY

        drawBird()
        drawPipe()
        updatePipe()

        c = stdscr.getch()

        if c == -1:
            # No key pressed
            charPositionY += 1  # gravity (or do nothing)

        elif c == ord('q'):
            break

        elif c == curses.KEY_UP or c == ord(' '):
            charPositionY -= 4
        
        stdscr.refresh()

        if charPositionY <= 0 or charPositionY >= height:
            print("bird y: " + str(charPositionY) + "\n")
            gameEnd()

        score += 1

        # Game speed
        time.sleep(0.2)
    
# Run
if __name__ == "__main__":
    wrapper(main)