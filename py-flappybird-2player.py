#!/usr/bin/env python3
import curses
from curses import wrapper
import random
import time

running = True

# Player one
char1PositionX = 10 
char1PositionY = 5 
player1Alive = True
scoreP1 = 0

# Player two
char2PositionX = 8
char2PositionY = 5
player2Alive = True
scoreP2 = 0

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
            # If the players are alive, draw them
            if (player1Alive):
                stdscr.addch(char1PositionY, char1PositionX, 'O', curses.color_pair(1) | curses.A_BOLD)
            
            if (player2Alive):
                stdscr.addch(char2PositionY, char2PositionX, 'O', curses.color_pair(1) | curses.A_BOLD)
                
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

        height, width = stdscr.getmaxyx()

        if not pipes or pipes[-1]['x'] < width - 20:
            top_height = random.randint(2, height - pipeGap - 2)
            bottom_start = top_height + pipeGap
            pipes.append({
                'x': width - 1,
                'top_height': top_height,
                'bottom_start': bottom_start
            })

    def checkCollision():
        global player2Alive
        global player1Alive
        for pipe in pipes[:]:
            if char1PositionX >= pipe['x'] and char1PositionX <= pipe['x'] + pipeWidth:
                #If both players die at the same time
                if char1PositionY < pipe['top_height'] or char1PositionY >= pipe['bottom_start'] and char2PositionY < pipe['top_height'] or char2PositionY >= pipe['bottom_start']:
                    gameEnd()
                # If player1 dies
                elif char1PositionY < pipe['top_height'] or char1PositionY >= pipe['bottom_start']:
                    player1Alive = False
                # If player2 dies
                elif char2PositionY < pipe['top_height'] or char2PositionY >= pipe['bottom_start']:
                    player2Alive = False
        
    def gameEnd():
        global scoreP1, scoreP2, running
        
        # Standard curses display logic
        stdscr.clear() 
        try:
            # Note: The order is usually (y, x) in curses
            stdscr.addstr(3, 2, "Game Over")
            stdscr.addstr(4, 2, "Player 1's score: " + str(scoreP1))
            stdscr.addstr(5, 2, "Player 2's score: " + str(scoreP2))
            stdscr.addstr(7, 2, "Press 'q' to exit...")
            stdscr.refresh()
        except curses.error:
            pass

        # The Loop: Pause and wait for 'q'
        while True:
            char = stdscr.getch()
            if char == ord('q'):
                break

        running = False

    while running:
        # Bring proper variables into scope
        global scoreP1
        global scoreP2
        global char1PositionY
        global char2PositionY
        global player1Alive
        global player2Alive

        # If player1 has moved out of bounds, kill them
        if char1PositionY <= 0 or char1PositionY >= height:
            player1Alive = False

        # If player2 has moved out of bounds, kill them
        if char2PositionY <= 0 or char2PositionY >= height:
            player2Alive = False

        # If both players are dead, end the game
        if (not player1Alive and not player2Alive):
            gameEnd()
        elif (not player2Alive):
            scoreP1 += 1
        elif (not player1Alive):
            scoreP2 += 1
        else:
            scoreP1 += 1
            scoreP2 += 2

        stdscr.nodelay(True)
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.refresh()

        drawBird()
        drawPipe()
        updatePipe()
        checkCollision()

        c = stdscr.getch()

        # If the user has not entered the up key, go down
        if (c != curses.KEY_UP):
            # No key pressed
            char1PositionY += 1  # gravity (or do nothing)
        else:
            # Key pressed
            char1PositionY -= 4

        if (c != ord(' ')):
            # Key not pressed
            char2PositionY += 1
        else:
            # Key pressed
            char2PositionY -= 5

        if c == ord('q'):
            break
            
        stdscr.refresh()
            
        # Game speed
        time.sleep(0.15)
    
# Run
if __name__ == "__main__":
    wrapper(main)