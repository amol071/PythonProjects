import pygame
import random
from PIL import Image, ImageDraw

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_JUMP = 5
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_HEIGHT = 400  # Added PIPE_HEIGHT constant

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))


# Function to create a pipe image with a gap
def create_pipe_image():
    pipe_img = Image.new("RGB", (PIPE_WIDTH, SCREEN_HEIGHT), (255, 255, 255))  # White background
    draw = ImageDraw.Draw(pipe_img)

    # Calculate the positions for the top and bottom rectangles
    gap_top = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)  # Randomize gap position
    gap_bottom = gap_top + PIPE_GAP

    # Draw top part of the pipe
    draw.rectangle([0, 0, PIPE_WIDTH, gap_top], fill=(0, 128, 0))  # Green color

    # Draw bottom part of the pipe
    draw.rectangle([0, gap_bottom, PIPE_WIDTH, SCREEN_HEIGHT], fill=(0, 128, 0))  # Green color

    pipe_img.save("pipe.png")
    return pygame.image.load("pipe.png")


# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.vel_y = 0
        self.radius = 25
        self.alive = True

    def flap(self):
        self.vel_y = -BIRD_JUMP

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.alive = False

    def draw(self):
        screen.blit(bird_img, (self.x - self.radius, self.y - self.radius))


# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_top = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)  # Adjusted range for the gap_top
        self.gap_bottom = self.gap_top + PIPE_GAP
        self.pipe_img = create_pipe_image()

    def move(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def draw(self):
        # Draw top pipe
        top_pipe_height = self.gap_top - PIPE_HEIGHT
        screen.blit(self.pipe_img, (self.x, top_pipe_height))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_bottom
        screen.blit(pygame.transform.flip(self.pipe_img, False, True), (self.x, bottom_pipe_y))


# Function to check collisions
def check_collision(bird, pipes):
    if bird.y - bird.radius < 0 or bird.y + bird.radius > SCREEN_HEIGHT:
        return True

    # Check collision with the ground
    if bird.y + bird.radius >= SCREEN_HEIGHT:
        return True

    for pipe in pipes:
        if bird.x + bird.radius > pipe.x and bird.x - bird.radius < pipe.x + PIPE_WIDTH:
            if bird.y - bird.radius < pipe.gap_top or bird.y + bird.radius > pipe.gap_bottom:
                return True
    return False


# Main function
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(2)]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()
        bird.draw()

        for pipe in pipes:
            pipe.move()
            pipe.draw()

            if pipe.x < bird.x and not pipe.off_screen():
                score += 0.5

            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))

        if check_collision(bird, pipes):
            running = False

        pygame.display.update()
        clock.tick(60)

    print("Game Over")
    print("Your score:", int(score))
    pygame.quit()


if __name__ == "__main__":
    main()
