#!/usr/bin/env python3
"""
Flappy Bird CLI Game using curses
"""

import curses
import random
import time
from curses import wrapper

class FlappyBird:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

        # Game constants
        self.bird_x = 10
        self.bird_y = self.height // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.flap_strength = -2

        # Pipe settings
        self.pipe_width = 4
        self.pipe_gap = 8
        self.pipe_speed = 1
        self.pipes = []

        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False

        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Bird
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Pipes
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Game over
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Score

    def draw_bird(self):
        """Draw the bird"""
        try:
            self.stdscr.addch(int(self.bird_y), self.bird_x, 'O', curses.color_pair(1))
        except curses.error:
            pass  # Ignore if out of bounds

    def draw_pipes(self):
        """Draw all pipes"""
        for pipe in self.pipes:
            pipe_x = pipe['x']

            # Top pipe
            for y in range(pipe['top_height']):
                try:
                    self.stdscr.addch(y, pipe_x, '|', curses.color_pair(2))
                    self.stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(2))
                except curses.error:
                    pass

            # Bottom pipe
            for y in range(pipe['bottom_start'], self.height - 1):
                try:
                    self.stdscr.addch(y, pipe_x, '|', curses.color_pair(2))
                    self.stdscr.addch(y, pipe_x + 1, '|', curses.color_pair(2))
                except curses.error:
                    pass

    def update_bird(self):
        """Update bird position and velocity"""
        if not self.game_over and not self.paused:
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity

            # Check boundaries
            if self.bird_y < 0 or self.bird_y >= self.height - 1:
                self.game_over = True

    def update_pipes(self):
        """Update pipe positions and add new pipes"""
        if not self.game_over and not self.paused:
            # Move existing pipes
            for pipe in self.pipes[:]:
                pipe['x'] -= self.pipe_speed
                if pipe['x'] + self.pipe_width < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

            # Add new pipe
            if not self.pipes or self.pipes[-1]['x'] < self.width - 20:
                top_height = random.randint(2, self.height - self.pipe_gap - 2)
                bottom_start = top_height + self.pipe_gap
                self.pipes.append({
                    'x': self.width - 1,
                    'top_height': top_height,
                    'bottom_start': bottom_start
                })

    def check_collisions(self):
        """Check for collisions with pipes"""
        if self.game_over or self.paused:
            return

        bird_left = self.bird_x
        bird_right = self.bird_x
        bird_top = int(self.bird_y)
        bird_bottom = int(self.bird_y)

        for pipe in self.pipes:
            pipe_left = pipe['x']
            pipe_right = pipe['x'] + self.pipe_width - 1

            # Check horizontal overlap
            if bird_right >= pipe_left and bird_left <= pipe_right:
                # Check vertical collision with top pipe
                if bird_top <= pipe['top_height']:
                    self.game_over = True
                    return
                # Check vertical collision with bottom pipe
                if bird_bottom >= pipe['bottom_start']:
                    self.game_over = True
                    return

    def draw_score(self):
        """Draw the current score"""
        score_text = f"Score: {self.score}"
        try:
            self.stdscr.addstr(0, self.width - len(score_text) - 1, score_text, curses.color_pair(4))
        except curses.error:
            pass

    def draw_instructions(self):
        """Draw game instructions"""
        instructions = "SPACE/UP: Flap | P: Pause | Q: Quit"
        try:
            self.stdscr.addstr(self.height - 1, 0, instructions)
        except curses.error:
            pass

    def draw_game_over(self):
        """Draw game over screen"""
        game_over_text = "GAME OVER!"
        final_score_text = f"Final Score: {self.score}"
        restart_text = "Press R to restart or Q to quit"

        try:
            self.stdscr.addstr(self.height // 2 - 2, self.width // 2 - len(game_over_text) // 2,
                              game_over_text, curses.color_pair(3) | curses.A_BOLD)
            self.stdscr.addstr(self.height // 2, self.width // 2 - len(final_score_text) // 2,
                              final_score_text, curses.color_pair(4))
            self.stdscr.addstr(self.height // 2 + 2, self.width // 2 - len(restart_text) // 2,
                              restart_text)
        except curses.error:
            pass

    def reset_game(self):
        """Reset the game state"""
        self.bird_y = self.height // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.paused = False

    def run(self):
        """Main game loop"""
        self.stdscr.nodelay(True)  # Non-blocking input
        curses.curs_set(0)  # Hide cursor

        while True:
            self.stdscr.clear()

            # Handle input
            try:
                key = self.stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord(' ') or key == curses.KEY_UP:
                    if not self.game_over and not self.paused:
                        self.bird_velocity = self.flap_strength
                elif key == ord('p'):
                    self.paused = not self.paused
                elif key == ord('r') and self.game_over:
                    self.reset_game()
            except curses.error:
                pass  # No input available

            # Update game state
            self.update_bird()
            self.update_pipes()
            self.check_collisions()

            # Draw everything
            self.draw_pipes()
            self.draw_bird()
            self.draw_score()
            self.draw_instructions()

            if self.game_over:
                self.draw_game_over()

            self.stdscr.refresh()

            # Game speed
            time.sleep(0.1)

def main(stdscr):
    game = FlappyBird(stdscr)
    game.run()

if __name__ == "__main__":
    wrapper(main)