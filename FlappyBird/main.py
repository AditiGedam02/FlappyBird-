import pygame, random, sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Bird setup
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.6
jump_strength = -10

# Pipes
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []  # stores (x, top_height)

# Game variables
score = 0
game_active = True

def create_pipe():
    top_height = random.randint(100, 400)
    pipes.append([WIDTH, top_height])

def draw_pipes():
    for pipe in pipes:
        x = pipe[0]
        top_height = pipe[1]
        pygame.draw.rect(screen, GREEN, (x, 0, pipe_width, top_height))
        pygame.draw.rect(screen, GREEN, (x, top_height + pipe_gap, pipe_width, HEIGHT - (top_height + pipe_gap)))

def move_pipes():
    global score
    for pipe in pipes:
        pipe[0] -= pipe_speed
        # Count score
        if pipe[0] + pipe_width == bird_x:
            score += 1
    # Remove pipes that go off screen
    if pipes and pipes[0][0] < -pipe_width:
        pipes.pop(0)

def check_collision():
    # Ground or ceiling
    if bird_y + bird_radius > HEIGHT or bird_y - bird_radius < 0:
        return False
    # Pipes
    for pipe in pipes:
        x = pipe[0]
        top_height = pipe[1]
        if x < bird_x + bird_radius < x + pipe_width:
            if bird_y - bird_radius < top_height or bird_y + bird_radius > top_height + pipe_gap:
                return False
    return True

# Game loop
running = True
spawn_timer = 0

while running:
    clock.tick(60)
    screen.fill(BLUE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_velocity = jump_strength
            if event.key == pygame.K_r and not game_active:
                # Reset game
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipes.clear()
                score = 0
                game_active = True

    if game_active:
        # Bird motion
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe management
        spawn_timer += 1
        if spawn_timer > 90:
            create_pipe()
            spawn_timer = 0
        move_pipes()

        # Check collisions
        if not check_collision():
            game_active = False

        # Draw bird and pipes
        pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)
        draw_pipes()

        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Game Over screen
        over_text = font.render("Game Over! Press R to Restart", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(over_text, (20, HEIGHT//2 - 40))
        screen.blit(score_text, (120, HEIGHT//2))

    pygame.display.flip()
