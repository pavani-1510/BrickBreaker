import pygame
import sys
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8

# Ball
BALL_RADIUS = 10
BALL_SPEED = 3.5

# Bricks
BRICK_ROWS = 1
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PADDLE_WIDTH))

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-1, 1]) * BALL_SPEED
        self.dy = -BALL_SPEED

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)

    def rect(self):
        return pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

def create_bricks(rows=BRICK_ROWS):
    bricks = []
    colors = [GREEN, YELLOW, BLUE, RED, WHITE, (255, 128, 0)]
    for row in range(rows):
        for col in range(BRICK_COLS):
            x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
            y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
            color = colors[row % len(colors)]
            bricks.append(Brick(x, y, color))
    return bricks

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    current_rows = BRICK_ROWS
    level = 1
    score = 0
    lives = 3
    game_over = False
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Restart game
                    paddle = Paddle()
                    ball = Ball()
                    bricks = create_bricks()
                    score = 0
                    lives = 3
                    game_over = False
                    win = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move('left')
        if keys[pygame.K_RIGHT]:
            paddle.move('right')

        if not game_over:
            ball.move()

            # Ball collision with walls
            if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= SCREEN_WIDTH:
                ball.dx *= -1
            if ball.y - BALL_RADIUS <= 0:
                ball.dy *= -1
            if ball.y + BALL_RADIUS >= SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.reset()
                else:
                    game_over = True

            # Ball collision with paddle
            if ball.rect().colliderect(paddle.rect):
                ball.dy *= -1
                # Add some control based on where the ball hits the paddle
                offset = (ball.x - paddle.rect.centerx) / (PADDLE_WIDTH // 2)
                ball.dx = BALL_SPEED * offset

            # Ball collision with bricks
            for brick in bricks:
                if brick.alive and ball.rect().colliderect(brick.rect):
                    brick.alive = False
                    score += 10
                    ball.dy *= -1
                    break

            if all(not brick.alive for brick in bricks):
                # Add 5 more rows at the top and continue to next level
                level += 1
                # Shift all existing bricks down by 5 rows height
                shift_y = 5 * (BRICK_HEIGHT + BRICK_PADDING)
                for brick in bricks:
                    brick.rect.y += shift_y
                # Create 5 new rows at the top
                new_bricks = []
                colors = [GREEN, YELLOW, BLUE, RED, WHITE, (255, 128, 0)]
                for row in range(5):
                    for col in range(BRICK_COLS):
                        x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                        y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                        color = colors[row % len(colors)]
                        new_bricks.append(Brick(x, y, color))
                bricks = new_bricks + bricks
                ball.reset()

        # Drawing
        screen.fill(BLACK)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

        if game_over:
            msg = "Game Over"
            msg_text = font.render(msg, True, YELLOW)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
