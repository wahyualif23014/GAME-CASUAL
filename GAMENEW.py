import pygame
import random

# Inisialisasi pygame
pygame.init()

# Konstanta layar
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Warna
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load assets
BIRD_IMG = pygame.image.load("assets/bird.png")  
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (50, 35))

PIPE_IMG = pygame.image.load("assets/pipe.png")  
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (70, 400))

# Load multiple backgrounds for dynamic effect
BACKGROUND_IMAGES = [
    pygame.image.load("assets/background.jpg"),
    pygame.image.load("assets/BG4.png"),
    pygame.image.load("assets/BG5.png")
]
BACKGROUND_IMAGES = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in BACKGROUND_IMAGES]

# Load sound effects
JUMP_SOUND = pygame.mixer.Sound("assets/jumpwav.wav")  
GAME_OVER_SOUND = pygame.mixer.Sound("assets/gameover.wav") 
pygame.mixer.music.load("assets/background_music.mp3")  
pygame.mixer.music.play(-1)  

# Kesulitan game
gravity = 0.8 
jump_strength = -8
pipe_gap = 150
pipe_speed = 3

def create_pipe():
    y = random.randint(200, 400)
    return {'x': WIDTH, 'y': y}

def draw_pipes(pipes):
    for pipe in pipes:
        SCREEN.blit(PIPE_IMG, (pipe['x'], pipe['y']))
        SCREEN.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y'] - pipe_gap - PIPE_IMG.get_height()))

def check_collision(bird_y, pipes):
    for pipe in pipes:
        if pipe['x'] < 100 < pipe['x'] + 70:
            if bird_y < pipe['y'] - pipe_gap or bird_y + 35 > pipe['y']:
                return True
    return False

def show_message(text, size, color, y_offset):
    font = pygame.font.Font(None, size)
    message = font.render(text, True, color)
    SCREEN.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 + y_offset))

def main_menu():
    running = True
    while running:
        SCREEN.fill(BLUE)
        SCREEN.blit(BACKGROUND_IMAGES[0], (0, 0))  # Use the first background
        show_message("Flappy Bird", 65, WHITE, -50)
        show_message("Press SPACE to Start", 36, BLUE, 50)
        show_message("Press ESC to Exit", 36, RED, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

def game_loop():
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipes = []
    clock = pygame.time.Clock()
    running = True

    while running:
        SCREEN.fill(BLUE)
        SCREEN.blit(BACKGROUND_IMAGES[score // 5 % len(BACKGROUND_IMAGES)], (0, 0))  # Change background based on score
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                    JUMP_SOUND.play()  
        
        bird_velocity += gravity
        bird_y += bird_velocity
        
        # Pipa bergerak
        for pipe in pipes:
            pipe['x'] -= pipe_speed
        
        if len(pipes) == 0 or pipes[-1]['x'] < WIDTH - 200:
            pipes.append(create_pipe())
        
        if pipes and pipes[0]['x'] < -70:
            pipes.pop(0)
            score += 1
        
        if check_collision(bird_y, pipes) or bird_y > HEIGHT - 50 or bird_y < 0:
            GAME_OVER_SOUND.play() 
            running = False
        
        draw_pipes(pipes)
        SCREEN.blit(BIRD_IMG, (100, bird_y))
        
        # Skor
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(text, (10, 10))
        
        pygame.display.update()
        clock.tick(30)

    game_over(score)

def game_over(score):
    running = True
    while running:
        SCREEN.fill(BLUE)
        SCREEN.blit(BACKGROUND_IMAGES[0], (0, 0))
        show_message("Game Over", 64, RED, -50)
        show_message(f"Score: {score}", 36, WHITE, 50)
        show_message("Press R to Restart", 36, WHITE, 100)
        show_message("Press ESC to Exit", 36, RED, 150)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

if __name__ == "__main__":
    main_menu()

pygame.quit()