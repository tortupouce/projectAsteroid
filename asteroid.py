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
SHOOT_COOLDOWN = 0.3



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
def get_ship_char(angle):
    if 45 <= angle < 135:
        return '<'
    elif 135 <= angle < 225:
        return 'v'
    elif 225 <= angle < 315:
        return '>'
    else:
        return '^'


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    max_y, max_x = stdscr.getmaxyx()
    ship_x = max_x // 2
    ship_angle = 0
    ship_dx = 0
    ship_dy = 0

    ship_y = max_y // 2
    bullets = []
    last_shot_time = 0

    asteroids = [GameObject(
        random.randint(0, max_x - 1),
        random.randint(0, max_y - 1),
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        ASTEROID_CHAR
    ) for _ in range(ASTEROID_COUNT)]

    while True:
        ship_x = (ship_x + ship_dx) % max_x
        ship_y = (ship_y + ship_dy) % max_y

        stdscr.clear()
        stdscr.addstr(0, 0, "Click to shoot. Press 'q' to quit.")
        stdscr.addch(int(ship_y), int(ship_x), get_ship_char(ship_angle))



        for bullet in bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            if 0 <= int(bullet['x']) < max_x and 0 <= int(bullet['y']) < max_y:
                stdscr.addch(int(bullet['y']), int(bullet['x']), BULLET_CHAR)
            else:
                bullets.remove(bullet)

        for asteroid in asteroids:
            asteroid.move(max_x, max_y)
            asteroid.draw(stdscr)

        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if int(bullet['x']) == int(asteroid.x) and int(bullet['y']) == int(asteroid.y):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    break

        stdscr.refresh()
        key = stdscr.getch()
        current_time = time.time()

        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            ship_angle = (ship_angle - 10) % 360
        elif key == curses.KEY_RIGHT:
            ship_angle = (ship_angle + 10) % 360
        elif key == curses.KEY_UP:

            thrust_x = math.cos(math.radians(ship_angle)) * 0.2
            thrust_y = -math.sin(math.radians(ship_angle)) * 0.2
            ship_dx += thrust_x
            ship_dy += thrust_y

            max_speed = 2.5
            speed = math.hypot(ship_dx, ship_dy)
            if speed > max_speed:
                scale = max_speed / speed
                ship_dx *= scale
                ship_dy *= scale
        elif key == curses.KEY_DOWN:

            ship_dx *= 0.9
            ship_dy *= 0.9



        elif key == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_PRESSED:
                    if current_time - last_shot_time >= SHOOT_COOLDOWN:
                        dx = mx - ship_x
                        dy = ship_y - my
                        angle = math.atan2(dy, dx)
                        bullets.append({
                            'x': ship_x,
                            'y': ship_y,
                            'dx': math.cos(angle) * 2,
                            'dy': -math.sin(angle) * 2
                        })
                        last_shot_time = current_time
            except curses.error:
                pass

        time.sleep(0.05)



if __name__ == "__main__":
    curses.wrapper(main)
