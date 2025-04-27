import pygame
from sys import exit
from collections import deque
import random

pixel_size = 30
width, height = (480, 700)
box_x = (0, width//pixel_size - 1)
box_y = (0, height//pixel_size - 1)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#for convenience
directions = {  pygame.K_RIGHT: 'right', 
                pygame.K_LEFT: 'left',
                pygame.K_UP: 'up',
                pygame.K_DOWN: 'down'
              }
opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
angles = {'left': 180, 'right': 0, 'up': 90, 'down': 270}

class Coord(tuple):
    def __init__(self, pair):
        assert len(pair) == 2
        self.x, self. y = pair

    def shift(self):
        return self.x * pixel_size, self.y * pixel_size

def shift(pair):
    x, y = pair
    return x * pixel_size, y * pixel_size

class Snake:
    def __init__(self):
        self.length = START_LEN
        self.speed = 1
        self.moves = {'right': self.move_right, 'left': self.move_left, 'up': self.move_up, 'down': self.move_down}
        self.move_queue = deque()
        self.segments = deque() 
        self.directions = deque() 
        height = random.randint(*box_y)
        for i in range(self.length):
            self.segments.append((i, height))
            self.directions.append('right')
        self.moved = 0 #how much of a pixel traveled

    def display(self):
        for coord in self.segments:
            screen.blit(SNAKE_BLOCK, shift(coord))
        #self.display_tail()
        #self.display_head()

    def grow(self):
        if SNAKE.length == MAX_LEN: return
        tail_x, tail_y = self.segments[0]
        tail_facing = self.directions[0]
        new_tail = ()
        if tail_facing == 'right':
            new_tail = (wrap_x(tail_x - 1), tail_y)
        elif tail_facing == 'left':
            new_tail = (wrap_x(tail_x + 1), tail_y)
        elif tail_facing == 'up':
            new_tail = (tail_x, wrap_y(tail_y + 1))
        elif tail_facing == 'down':
            new_tail = (tail_x, wrap_y(tail_y - 1))

        self.segments.appendleft(new_tail)
        self.directions.appendleft(tail_facing)
        self.length += 1

    def is_valid(self, key):
        facing = self.directions[-1]
        return key in directions and directions[key] != facing and \
            directions[key] != opposites[self.directions[-2] if self.move_queue == deque() else self.move_queue[-1]] and \
            directions[key] != opposites[facing]


    def move(self, key):
        self.moved += pos_change
        if self.move_queue == deque():
            if self.is_valid(key):
                    if self.moved < 0.5:
                        self.moved = 0
                        self.directions[-1] = directions[key]
                    else:
                        self.move_queue.append(directions[key])
        else:
            if self.is_valid(key) and directions[key] != self.move_queue[-1]:
                self.move_queue.append(directions[key])
            if self.moved < 0.5:
                self.moved = 0
                self.directions[-1] = self.move_queue.popleft()




        if self.moved > 1:
            self.moved -= 1
        else:
            return

        for i in range(self.length - 1):
            self.segments[i] = self.segments[i + 1]

        for i in range(self.length - 1):
            self.directions[i] = self.directions[i + 1]

        self.moves[self.directions[-1]]()


    '''
    def display_tail(self):
        tail_facing = self.directions[0] 
        angles[opposites[tail_facing]]
        #draw_triangle 
        pass

    def display_head(self):
        head_facing = self.directions[0] 
        angles[opposites[head_facing]]
        #draw semicircle
        pass
    '''

    def move_right(self):
         head = self.segments[-1]
         self.segments[-1] = wrap_x(head[0] + 1), head[1]

    def move_left(self):
        head = self.segments[-1]
        self.segments[-1] = wrap_x(head[0] - 1), head[1]

    def move_up(self):
        head = self.segments[-1]
        self.segments[-1] = head[0], wrap_y(head[1] - 1)

    def move_down(self):
        head = self.segments[-1]
        self.segments[-1] = head[0], wrap_y(head[1] + 1)

    def biting(self, point):
        return self.segments[-1] == point

    def biting_self(self):
        head = self.segments[-1]
        for i in range(self.length - 1):
            if head == self.segments[i]:
                return True
        return False

def wrap_x(x):
    return x % (box_x[1] - box_x[0]) + box_x[0]

def wrap_y(y):
    return y % (box_y[1] - box_y[0]) + box_y[0]

def spawn_food():
    while True:
        food = (random.randint(box_x[0] + 1, box_x[1] - 1), random.randint(box_y[0] + 1, box_y[1] - 1))
        if food not in SNAKE.segments:
            return Coord(food)


SNAKE_BLOCK = pygame.Surface((pixel_size, pixel_size))
SNAKE_BLOCK.fill('#1B341D')

FOOD_BLOCK = pygame.Surface((pixel_size, pixel_size))
FOOD_BLOCK.fill('#1B341D')

START_LEN = 2
MAX_LEN = START_LEN + 10
GOAL = 10
SNAKE = Snake()
food = None
score = 0
game_state = 'running'
FRAME_RATE = 60
velocity = 6
pos_change = velocity/FRAME_RATE

pygame.font.init()
font = pygame.font.Font(None, 35)
game_over_msg = font.render('Game Over', False, 'Green')
game_over_rect = game_over_msg.get_rect(center = (width/2, height/4))
game_clear_msg = font.render('You Win', False, 'Green')
game_clear_rect = game_clear_msg.get_rect(center = (width/2, height/4))

pygame.init()

while True:
    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_SPACE and (game_state == 'game_over' or game_state == 'game_clear'):
                SNAKE = Snake()
                food = None
                score = 0
                velocity = 6
                pos_change = velocity/FRAME_RATE
                game_state = 'running'

    if game_state == 'running':
        food = spawn_food() if food == None else food

        SNAKE.move(key)


        if SNAKE.biting(food):
            food = None
            score += 1
            SNAKE.grow()
            if score % 3 == 0:
                velocity += 1
                pos_change = velocity/FRAME_RATE

        score_msg = font.render(f'Score: {score}', False, '#1B341D')
        score_rect = score_msg.get_rect(topleft=(0,0))

        if SNAKE.biting_self():
            score_rect = score_msg.get_rect(center=(width/2,height/2))
            game_state = 'game_over'
            screen.fill('Red')


        if score == GOAL:
            game_state = 'game_clear'
            score_rect = score_msg.get_rect(center=(width/2,height/2))


        screen.fill('#50B156')
        SNAKE.display()
        screen.blit(score_msg, score_rect)
        if food:
            screen.blit(FOOD_BLOCK, food.shift())


    elif game_state == 'game_over':
        screen.fill('#50B156')
        screen.blit(game_over_msg, game_over_rect)
        screen.blit(score_msg, score_rect)

    elif game_state == 'game_clear':
        screen.fill('#50B156')
        screen.blit(game_clear_msg, game_clear_rect)
        screen.blit(score_msg, score_rect)

    pygame.display.update()
    clock.tick(FRAME_RATE)

