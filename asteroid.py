import curses
import math
import random
import time

# Constants
SHIP_CHAR = '^'
BULLET_CHAR = '.'
ASTEROID_CHAR = 'O'
MAX_BULLETS = 5
ASTEROID_COUNT = 5

class GameObject:
    def __init__(self, x, y, dx, dy, char):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.char = char

    def move(self, max_x, max_y):
        self.x = (self.x + self.dx) % max_x
        self.y = (self.y + self.dy) % max_y

    def draw(self, screen):
        screen.addch(int(self.y), int(self.x), self.char)

def angle_to_vector(angle):
    rad = math.radians(angle)
    return math.cos(rad), -math.sin(rad)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)
    curses.mousemask(1)


    max_y, max_x = stdscr.getmaxyx()
    ship_x = max_x // 2
    ship_y = max_y // 2
    ship_angle = 0
    bullets = []
    asteroids = [GameObject(random.randint(0, max_x - 1),
                            random.randint(0, max_y - 1),
                            random.uniform(-1, 1),
                            random.uniform(-1, 1),
                            ASTEROID_CHAR) for _ in range(ASTEROID_COUNT)]

    while True:
        stdscr.clear()

        stdscr.addch(int(ship_y), int(ship_x), SHIP_CHAR)

        # move bullets
        for bullet in bullets[:]:
            bullet.move(max_x, max_y)
            bullet.draw(stdscr)
            # Remove bullet (doesn't seem to work)
            if not (0 <= bullet.x < max_x and 0 <= bullet.y < max_y):
                bullets.remove(bullet)

        # Move ass
        for asteroid in asteroids:
            asteroid.move(max_x, max_y)
            asteroid.draw(stdscr)

        # Collision detection
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if int(bullet.x) == int(asteroid.x) and int(bullet.y) == int(asteroid.y):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    break

        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            ship_angle = (ship_angle - 10) % 360
        elif key == curses.KEY_RIGHT:
            ship_angle = (ship_angle + 10) % 360
        elif key == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            dx = mx - ship_x
            dy = ship_y - my
            angle = math.degrees(math.atan2(dy, dx))
            rad = math.radians(angle)
            vx = math.cos(rad) * 2
            vy = -math.sin(rad) * 2
            if len(bullets) < MAX_BULLETS:
                bullets.append(GameObject(ship_x, ship_y, vx, vy, BULLET_CHAR))





        stdscr.refresh()
        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(main)
