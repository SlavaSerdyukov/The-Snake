from random import choice, randint

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
DEFAULT_COLOR = (255, 255, 255)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position_x=0, position_y=0, body_color=DEFAULT_COLOR):
        """Инициализация игрового объекта."""
        self.position_x = position_x
        self.position_y = position_y
        self.body_color = body_color

    @property
    def position(self):
        """Возвращает текущую позицию объекта."""
        return self.position_x, self.position_y

    def draw(self, surface):
        """Отрисовка объекта на поверхности."""
        pygame.draw.rect(
            surface,
            self.body_color,
            (self.position_x * GRID_SIZE, self.position_y
             * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )


class Apple(GameObject):
    """Класс для объекта 'Яблоко'."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(randint(0, GRID_WIDTH - 1),
                         randint(0, GRID_HEIGHT - 1), APPLE_COLOR)

    def randomize_position(self, occupied_positions=None):
        """Случайным образом меняет яблоко, избегая занятых позиций."""
        if occupied_positions is None:
            occupied_positions = set()
        while True:
            self.position_x = randint(0, GRID_WIDTH - 1)
            self.position_y = randint(0, GRID_HEIGHT - 1)
            if (self.position_x, self.position_y) not in occupied_positions:
                break


class Snake(GameObject):
    """Класс для объекта 'Змейка'."""

    OPPOSITE_DIRECTIONS = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(GRID_WIDTH // 2, GRID_HEIGHT // 2, SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сброс положения змейки к начальному."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def update_direction(self, new_direction):
        """Обновление направления движения змейки."""
        if new_direction != self.OPPOSITE_DIRECTIONS.get(self.direction):
            self.direction = new_direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки."""
        head = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = (
            (head[0] + delta_x) % GRID_WIDTH,
            (head[1] + delta_y) % GRID_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def has_collided(self):
        """Проверка столкновения змейки с самой собой."""
        head = self.get_head_position()
        return head in self.positions[1:]


def handle_keys(snake):
    """Обработка событий пользовательского ввода."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Главная функция игры."""
    pygame.init()
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        if snake.has_collided():
            snake.reset()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        game_screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(game_screen)
        apple.draw(game_screen)
        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
