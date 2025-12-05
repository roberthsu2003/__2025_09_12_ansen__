import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)
GRAY = (40, 40, 40)

START_FPS = 7
MAX_FPS = 15


def get_speed(score):
    speed = START_FPS + (score // 30)
    return min(speed, MAX_FPS)


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font("NotoSansTC-Regular.ttf", 36)
big_font = pygame.font.Font("NotoSansTC-Regular.ttf", 72)


class Snake:

    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True
        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            rect = pygame.Rect(x, y, GRID_SIZE - 2, GRID_SIZE - 2)
            if i == 0:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 2)
            else:
                pygame.draw.rect(surface, DARK_GREEN, rect)


class Food:

    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_body=None):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.position = (x, y)
            if snake_body is None or self.position not in snake_body:
                break

    def draw(self, surface):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        rect = pygame.Rect(x, y, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_score(surface, score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def draw_game_over(surface, score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    game_over_text = big_font.render("遊戲結束", True, RED)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                WINDOW_HEIGHT // 2 - 50))
    surface.blit(game_over_text, text_rect)

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2,
                                             WINDOW_HEIGHT // 2 + 20))
    surface.blit(score_text, score_rect)

    restart_text = font.render("Press SPACE to restart or ESC to quit", True,
                               WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                 WINDOW_HEIGHT // 2 + 70))
    surface.blit(restart_text, restart_rect)


def draw_start_screen(surface):
    surface.fill(BLACK)

    title_text = big_font.render("SNAKE GAME", True, GREEN)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2,
                                             WINDOW_HEIGHT // 2 - 50))
    surface.blit(title_text, title_rect)

    start_text = font.render("Press SPACE to start", True, WHITE)
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2,
                                             WINDOW_HEIGHT // 2 + 30))
    surface.blit(start_text, start_rect)

    controls_text = font.render("Use arrow keys to move", True, GRAY)
    controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                   WINDOW_HEIGHT // 2 + 80))
    surface.blit(controls_text, controls_rect)


def main():
    snake = Snake()
    food = Food()
    food.spawn(snake.body)
    score = 0
    game_state = "start"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_state == "start":
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"

                elif game_state == "playing":
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))

                elif game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.spawn(snake.body)
                        score = 0
                        game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        if game_state == "playing":
            snake.move()

            if snake.check_collision():
                game_state = "game_over"

            if snake.body[0] == food.position:
                snake.grow = True
                score += 10
                food.spawn(snake.body)

        screen.fill(BLACK)

        if game_state == "start":
            draw_start_screen(screen)
        elif game_state == "playing":
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
        elif game_state == "game_over":
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
            draw_game_over(screen, score)

        pygame.display.flip()
        clock.tick(get_speed(score))


if __name__ == "__main__":
    main()
