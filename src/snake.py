"""Snake game"""
import enum
import random
import time
import pygame

FPS = 5
BLOCKSIZE = 20
SCREEN_W = 40
SCREEN_H = 30

COLOR_BACKGROUND = pygame.Color(255, 255, 255)
COLOR_SNAKE = pygame.Color(0, 0, 255)
COLOR_FOOD = pygame.Color(100, 255, 100)
COLOR_TEXT = pygame.Color(0, 200, 0)


class Direction(enum.Enum):
    """Definition for directions"""

    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Food:
    """Food representation"""

    def __init__(self) -> None:
        self.x = random.randrange(1, (SCREEN_W))
        self.y = random.randrange(1, (SCREEN_H))

    def get_position(self):
        """Get food position"""
        return [self.x, self.y]


class Snake:
    """Snake"""

    def __init__(self) -> None:
        self.head = [1, SCREEN_H // 2]
        self.body = [[1, SCREEN_H // 2], [0, SCREEN_H // 2]]

    def move(self, direction):
        """Move in direction"""
        match direction:
            case Direction.UP:
                self.head[1] -= 1
            case Direction.DOWN:
                self.head[1] += 1
            case Direction.LEFT:
                self.head[0] -= 1
            case Direction.RIGHT:
                self.head[0] += 1
        self.body.insert(0, self.head[:])

    def eat(self, food):
        """Eat food if can reach eat, return remaining food"""
        if self.head == food.get_position():
            food = None
        else:
            self.body.pop()
        return food

    def is_valid(self):
        """Check if snake's position is valid"""
        return (
            0 <= self.head[0] < SCREEN_W - 1
            and 0 <= self.head[1] < SCREEN_H - 1
            and self.head not in self.body[1:]
        )


class GameEngine:
    """The game"""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Snake Python")
        self.screen = pygame.display.set_mode(
            (SCREEN_W * BLOCKSIZE, SCREEN_H * BLOCKSIZE)
        )
        self.frame_per_sec = pygame.time.Clock()

    def get_user_input(self, game_on, direction):
        """Get user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != Direction.DOWN:
                    direction = Direction.UP
                if event.key == pygame.K_DOWN and direction != Direction.UP:
                    direction = Direction.DOWN
                if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                    direction = Direction.LEFT
                if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                    direction = Direction.RIGHT
                if event.key == pygame.K_ESCAPE:
                    game_on = False
        return [game_on, direction]

    def paint_square(self, pos, color):
        """Draw a square block"""
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(pos[0] * BLOCKSIZE, pos[1] * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
        )

    def update_screen(self, snake, food):
        """Update screen"""
        self.screen.fill(COLOR_BACKGROUND)
        for i in snake.body:
            self.paint_square(i, COLOR_SNAKE)
        self.paint_square(food.get_position(), COLOR_FOOD)
        pygame.display.update()
        self.frame_per_sec.tick(FPS)

    def game_over(self):
        """Display game over message and deinitialise pygame"""
        msg = pygame.font.SysFont("DejaVu Sans", 50, bold=True).render(
            "GAME OVER", True, COLOR_TEXT
        )
        msg_rect = msg.get_rect()
        msg_rect.center = (SCREEN_W * BLOCKSIZE / 2, SCREEN_H * BLOCKSIZE / 2)
        self.screen.fill(COLOR_BACKGROUND)
        self.screen.blit(msg, msg_rect)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()


def main():
    """Application's entry point"""
    game = GameEngine()
    snake = Snake()
    food = Food()
    direction = Direction.RIGHT
    game_on = True

    while game_on:
        game_on, direction = game.get_user_input(game_on, direction)
        snake.move(direction)
        food = snake.eat(food)
        if food is None:
            food = Food()
        game.update_screen(snake, food)
        game_on = game_on and snake.is_valid()

    game.game_over()


if __name__ == "__main__":
    main()
