import random
import pygame
from pygame.math import Vector2
from time import sleep
import sys
import os

cell_number = 20
cell_size = 40


class FRUIT:
    def __init__(self):
        # create an x and y position
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # create a rectangle. Rect object is working with pixels but we want to work with grids.
        fruit_rect = pygame.Rect(
            int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        self.apple = pygame.image.load(os.path.join(
            "Graphics", "apple.png")).convert_alpha()
        screen.blit(self.apple, fruit_rect)

    def new_fruit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self) -> None:
        # store snake body positions in a list of vectors
        self.create_snake()
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound(
            os.path.join("Sound", "crunch.wav"))

        # All possible heads
        self.head_up = pygame.image.load(
            os.path.join("Graphics", "head_up.png")).convert_alpha()
        self.head_down = pygame.image.load(
            os.path.join("Graphics", "head_down.png")).convert_alpha()
        self.head_left = pygame.image.load(
            os.path.join("Graphics", "head_left.png")).convert_alpha()
        self.head_right = pygame.image.load(
            os.path.join("Graphics", "head_right.png")).convert_alpha()

        # All possible tails
        self.tail_up = pygame.image.load(
            os.path.join("Graphics", "tail_up.png")).convert_alpha()
        self.tail_down = pygame.image.load(
            os.path.join("Graphics", "tail_down.png")).convert_alpha()
        self.tail_left = pygame.image.load(
            os.path.join("Graphics", "tail_left.png")).convert_alpha()
        self.tail_right = pygame.image.load(
            os.path.join("Graphics", "tail_right.png")).convert_alpha()

        # Straigt body
        self.vertical_body = pygame.image.load(
            os.path.join("Graphics", "body_vertical.png")).convert_alpha()
        self.horizantal_body = pygame.image.load(
            os.path.join("Graphics", "body_horizontal.png")).convert_alpha()

        # Turning body
        self.body_tr = pygame.image.load(
            os.path.join("Graphics", "body_tr.png")).convert_alpha()
        self.body_tl = pygame.image.load(
            os.path.join("Graphics", "body_tl.png")).convert_alpha()
        self.body_br = pygame.image.load(
            os.path.join("Graphics", "body_br.png")).convert_alpha()
        self.body_bl = pygame.image.load(
            os.path.join("Graphics", "body_bl.png")).convert_alpha()

    def create_snake(self):
        self.body = [Vector2(i, 10) for i in range(10, 13)]
        self.direction = Vector2(-1, 0)

    def draw_head(self, block_rect):
        direction = self.body[0] - self.body[1]
        if direction == pygame.Vector2(1, 0):
            screen.blit(self.head_right, block_rect)
        elif direction == pygame.Vector2(-1, 0):
            screen.blit(self.head_left, block_rect)
        elif direction == pygame.Vector2(0, -1):
            screen.blit(self.head_up, block_rect)
        elif direction == pygame.Vector2(0, 1):
            screen.blit(self.head_down, block_rect)

    def draw_tail(self, block_rect):
        direction = self.body[-2] - self.body[-1]
        if direction == pygame.Vector2(-1, 0):
            screen.blit(self.tail_right, block_rect)
        elif direction == pygame.Vector2(1, 0):
            screen.blit(self.tail_left, block_rect)
        elif direction == pygame.Vector2(0, 1):
            screen.blit(self.tail_up, block_rect)
        elif direction == pygame.Vector2(0, -1):
            screen.blit(self.tail_down, block_rect)

    def draw_snake(self):
        for i, block in enumerate(self.body):
            # TODO 1: rect for position
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # TODO 2: snake direction
            # Draw head
            if i == 0:
                self.draw_head(block_rect)
            # Draw tail
            elif self.body[-1] == block:
                self.draw_tail(block_rect)
            # Draw body
            else:
                direction_b = self.body[i] - self.body[i-1]
                direction_f = self.body[i+1] - self.body[i]
                # Draw straight body
                if direction_f == direction_b:
                    if direction_f == pygame.Vector2(0, 1) or direction_f == pygame.Vector2(0, -1):
                        screen.blit(self.vertical_body, block_rect)
                    elif direction_f == pygame.Vector2(1, 0) or direction_f == pygame.Vector2(-1, 0):
                        screen.blit(self.horizantal_body, block_rect)
                else:
                    if (direction_f == pygame.Vector2(1, 0) and direction_b == pygame.Vector2(0, -1)) or (direction_f == pygame.Vector2(0, 1) and direction_b == pygame.Vector2(-1, 0)):
                        screen.blit(self.body_br, block_rect)

                    elif (direction_f == Vector2(-1, 0) and direction_b == Vector2(0, -1)) or (direction_f == Vector2(0, 1) and direction_b == Vector2(1, 0)):
                        screen.blit(self.body_bl, block_rect)

                    elif (direction_f == pygame.Vector2(-1, 0) and direction_b == pygame.Vector2(0, 1)) or (direction_f == pygame.Vector2(0, -1) and direction_b == pygame.Vector2(1, 0)):
                        screen.blit(self.body_tl, block_rect)

                    elif (direction_f == Vector2(0, -1) and direction_b == Vector2(-1, 0)) or (direction_f == Vector2(1, 0) and direction_b == Vector2(0, 1)):
                        screen.blit(self.body_tr, block_rect)

    def move_snake(self):
        if self.new_block:
            self.new_block = False
        else:
            self.body.pop()  # Remove the last element
        self.body.insert(0, self.body[0] + self.direction)

    def back_moving(self):
        if self.body[0] + self.direction == self.body[1]:
            return True
        else:
            return False

    def play_sound(self):
        self.crunch_sound.play()


class MAIN:
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()
        with open("highest_Score.txt") as f:   
            self.highest_score = int(f.read())

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(0, cell_number, 2):
            for col in range(cell_number):
                if col % 2 == 0:
                    filled_raw = row
                else:
                    filled_raw = row+1
                grass_rect = pygame.Rect(
                    filled_raw*cell_size, col*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, grass_color, grass_rect)

    def eat_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.play_sound()
            self.fruit.new_fruit()
            # make sure fruit is not under the snake
            while self.fruit.pos in self.snake.body:
                self.fruit.new_fruit()
            # increase length
            self.snake.new_block = True

    def draw_score(self):
        current_score = len(self.snake.body)-3
        score_text = str(current_score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        highest_score_y = int(cell_size*cell_number - 20)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.apple, apple_rect)
        if self.highest_score < current_score:
            self.highest_score = current_score
        highest_score_text = f"Higest score: {self.highest_score}"
        highest_score_surface = game_font.render(highest_score_text, True, (56, 74, 12))
        highest_score_x = int(cell_size*cell_number - 140)
        score_rect = highest_score_surface.get_rect(center=(highest_score_x, highest_score_y))
        screen.blit(highest_score_surface, score_rect)

    def check_game_over(self):
        head = self.snake.body[0]
        # Check if snack is outside.
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over()
        # Check if head collide with body
        elif head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        # pygame.quit()
        # sys.exit()
        with open("highest_Score.txt", "w") as f:   
            f.write(str(self.highest_score))
        sleep(1)
        self.snake.body.clear()
        self.snake.create_snake()
        self.fruit.new_fruit()

    def update(self):
        self.snake.move_snake()
        self.eat_fruit()
        self.check_game_over()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()


# initilate the game
if __name__ == "__main__":
    current_path = os.getcwd()
    if "snake" not in current_path:
        snake_path = list(filter(lambda x: "snake" in x, os.listdir()))[0]
        os.chdir(os.path.join(current_path, snake_path))

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    # We do not work pixels, instead with grids so we need to define grid size.
    cell_size = 40
    cell_number = 20
    FPS = 60
    screen = pygame.display.set_mode(
        (cell_size*cell_number, cell_size*cell_number))  # width, height
    clock = pygame.time.Clock()

    main_game = MAIN()

    dirc = {"up": Vector2(0, -1),
            "down": Vector2(0, 1),
            "right": Vector2(1, 0),
            "left": Vector2(-1, 0),
            }
    SCREEN_UPDATE = pygame.USEREVENT
    game_font = pygame.font.Font(os.path.join(
        "Font", "PoetsenOne-Regular.ttf"), 25)
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    # Create the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction != dirc["down"]:
                        main_game.snake.direction = dirc["up"]
                elif event.key == pygame.K_DOWN:
                    if main_game.snake.direction != dirc["up"]:
                        main_game.snake.direction = dirc["down"]
                elif event.key == pygame.K_RIGHT:
                    if main_game.snake.direction != dirc["left"]:
                        main_game.snake.direction = dirc["right"]
                elif event.key == pygame.K_LEFT:
                    if main_game.snake.direction != dirc["right"]:
                        main_game.snake.direction = dirc["left"]

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(FPS)
