import pygame
pygame.font.init()
pygame.mixer.init()

# #Setups
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
}

WIDTH, HEIGHT = 900, 500  # Screen parameters
spaceship_width, spaceship_height = 80, 80  # Spaceships size
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create custom screen
pygame.display.set_caption("First game")  # Window title
fps = 60  # Frames per second
vel = 5
max_bullets = 3
bullet_velocity = 8
red_bullets = []
yellow_bullets = []
fonts = {"health":pygame.font.SysFont("comicsans", 40),
        "winner": pygame.font.SysFont("comicsans", 100)}
sounds = {"hit": pygame.mixer.Sound("Assets/Grenade+1.mp3"),
          "fire":pygame.mixer.Sound("Assets/Gun+Silencer.mp3")}
# Create new events
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2
space = pygame.transform.scale(
    pygame.image.load("Assets/space.png"), (WIDTH, HEIGHT))
border = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# #load data from Assets folder
yellow_spaceship_image = pygame.image.load("Assets/spaceship_yellow.png")
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(
    yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load("Assets/spaceship_red.png")
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (spaceship_width, spaceship_height)), 270)


def auto_move(red, yellow):
    red.x += 1
    if not 0 < yellow.x < WIDTH or not 0 < red.x < WIDTH:
        return False
    else:
        return True


def yellow_move(yellow, keys_pressed):
    if keys_pressed[pygame.K_a] and yellow.x-vel >= 0:  # Left
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x+vel+spaceship_width <= border.x:  # Right
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y-vel >= 0:  # Up
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y+vel + spaceship_height <= HEIGHT:  # Down
        yellow.y += vel


def red_move(red, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and red.x-vel >= border.x:  # Left
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x+vel+spaceship_width <= WIDTH:  # Right
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y-vel >= 0:  # Up
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y+vel+spaceship_height <= HEIGHT:  # Down
        red.y += vel


def handle_bullet(yellow_bullets, red_bullets, yellow, red):
    """
    1 Move the bullet
    2 Handle collision
    3 Remove bullet when go outside screen
    """
    for bullet in yellow_bullets:
        bullet.x += bullet_velocity
        if red.colliderect(bullet):  # Check for collision
            pygame.event.post(pygame.event.Event(red_hit))  # Red player was hitted
            yellow_bullets.remove(bullet)  # remove the bullet
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_velocity
        if yellow.colliderect(bullet):  # Check for collision
            pygame.event.post(pygame.event.Event(yellow_hit))  # yellow player was hitted
            red_bullets.remove(bullet)  # remove the bullet
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    update display
    """
    # screen.fill(colors["white"])
    screen.blit(space, (0, 0))
    pygame.draw.rect(screen, colors["black"], border)  # Add the border
    red_health_text = fonts["health"].render(
        f"Health: {red_health}", 1, colors["white"])
    yellow_health_text = fonts["health"].render(
        f"Health: {yellow_health}", 1, colors["white"])
    screen.blit(red_health_text, (WIDTH-red_health_text.get_width()-10, 10))
    screen.blit(yellow_health_text, (10, 10))
    # Set the images on top of the rectangles so they move with it
    screen.blit(yellow_spaceship, (yellow.x, yellow.y))
    screen.blit(red_spaceship, (red.x, red.y))
    # Draw red bullet
    for bullet in red_bullets:
        pygame.draw.rect(screen, colors["red"], bullet)
    # Draw yellow bullet
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, colors["yellow"], bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text = fonts["winner"].render(text,1,colors["white"])
    screen.blit(draw_text, (int(WIDTH/2) - int(draw_text.get_width()/2), int(HEIGHT/2) - int(draw_text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(500)

def main():
    red = pygame.Rect(800, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    health = {"red": 10, "yellow": 10}
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            # #Close code if window closed
            if event.type == pygame.QUIT:
                run = False
                pass
            if event.type == red_hit:
                health['red'] = health['red']-1
                sounds["hit"].play()

            if event.type == yellow_hit:
                health['yellow'] = health['yellow']-1
                sounds["hit"].play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        yellow.x+yellow.width, yellow.y+yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    sounds["fire"].play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x, red.y+red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    sounds["fire"].play()

        
        # #Bullet hit

        winner_text = ""
        if health["red"] <= 0:
            winner_text = "Yellow Win!"
        elif health["yellow"] <= 0:
            winner_text = "Red Win!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        # #manual control
        keys_pressed = pygame.key.get_pressed()
        yellow_move(yellow, keys_pressed)
        red_move(red, keys_pressed)
        
        # #Bullet control
        handle_bullet(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    health["red"], health["yellow"])
    pygame.quit()


if __name__ == '__main__':
    main()
