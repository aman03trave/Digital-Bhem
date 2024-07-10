import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 15

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 200, 0)
DARK_RED = (200, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.head_color = YELLOW
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))
        
        # Check for collision with wall
        if new[0] < 0 or new[0] >= WINDOW_WIDTH or new[1] < 0 or new[1] >= WINDOW_HEIGHT:
            self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:
                # Draw the head
                pygame.draw.circle(surface, self.head_color, (int(p[0] + GRID_SIZE / 2), int(p[1] + GRID_SIZE / 2)), GRID_SIZE // 2 + self.length // 2)
                pygame.draw.circle(surface, DARK_YELLOW, (int(p[0] + GRID_SIZE / 2), int(p[1] + GRID_SIZE / 2)), GRID_SIZE // 2 + self.length // 2, 1)
            else:
                # Draw the body
                pygame.draw.circle(surface, self.color, (int(p[0] + GRID_SIZE / 2), int(p[1] + GRID_SIZE / 2)), GRID_SIZE // 2 + self.length // 4)
                pygame.draw.circle(surface, DARK_GREEN, (int(p[0] + GRID_SIZE / 2), int(p[1] + GRID_SIZE / 2)), GRID_SIZE // 2 + self.length // 4, 1)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.turn(UP)
        elif keys[pygame.K_DOWN]:
            self.turn(DOWN)
        elif keys[pygame.K_LEFT]:
            self.turn(LEFT)
        elif keys[pygame.K_RIGHT]:
            self.turn(RIGHT)

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0] + GRID_SIZE / 2), int(self.position[1] + GRID_SIZE / 2)), GRID_SIZE // 2)
        pygame.draw.circle(surface, DARK_RED, (int(self.position[0] + GRID_SIZE / 2), int(self.position[1] + GRID_SIZE / 2)), GRID_SIZE // 2, 1)

# Main function
def main():
    global CLOCK, SCREEN, FONT

    # Initialize game window
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont('Arial', 40)

    # Initialize snake and food
    snake = Snake()
    food = Food()

    # Game loop
    while True:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Handle user input
        snake.handle_keys()
        snake.move()

        # Check for collision with food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        # Draw snake, food, and score
        snake.draw(SCREEN)
        food.draw(SCREEN)
        score_text = FONT.render(f"Score: {snake.score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Update display and control FPS
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
