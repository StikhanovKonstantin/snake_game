from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (0, 204, 0)

# Цвет змейки
SNAKE_COLOR = (0, 0, 153)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Объявляем функцию handle keys, которая обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Объявляем родительсикй класс GameObject, в нем хранятся два метода."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод draw пустой - предполагает,
        что в доч. классах его переопределят.
        """
        pass


class Apple(GameObject):
    """Объявляем дочерний от GameObject класс Apple, с помощтю которого
    на игровом поле будет вырисовываться яблоко в случайной ячейке.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод предназачен для случайного определения яблочка на поле.
        Используется в инициализаторе класса, как значение position.
        """
        rand_screen_width = randint(0, GRID_WIDTH) * GRID_SIZE
        rand_screen_height = randint(0, GRID_HEIGHT) * GRID_SIZE
        self.position = (rand_screen_width,
                         rand_screen_height)
        return self.position

    def draw(self):
        """Переопределяем родительский метод draw.
        В нём описываем то, как будет выглядеть наше яблочко.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявляем дочерний от GameObject класс Snake. В нем описывается:
    инициализатор основных качеств змейки, а также методы, которые описывают
    передвижение, зарисовку, повороты и сброс змейки до начальных значений.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод, который задаёт новое направление нашей змейке."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод, который возвращает 1 элемент списка -
        которым является голова змейки.
        """
        return self.positions[0]

    def move(self):
        """Метод, отвечающий за передвижение змейки.
        В зависимости направления змейки, наша змейка(список) меняется,
        в начало добавляются новые координаты, а в конце - убираем старые.
        """
        current_head = self.get_head_position()
        new_head = (current_head[0] + self.direction[0] * GRID_SIZE,
                    current_head[1] + self.direction[1] * GRID_SIZE)

        # Обработка выхода за границы экрана
        if new_head[0] > SCREEN_WIDTH:
            new_head = (new_head[0] - SCREEN_WIDTH - 20, new_head[1])
        elif new_head[0] < 0:
            new_head = (new_head[0] + SCREEN_WIDTH, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], new_head[1] + SCREEN_HEIGHT + 20)
        elif new_head[1] > SCREEN_HEIGHT and new_head[1] % SCREEN_HEIGHT != 0:
            new_head = (new_head[0], new_head[1] % SCREEN_HEIGHT)

        # Добавляем новые координаты в начало списка
        self.positions.insert(0, new_head)

        # Удаляем последнюю координату, если длина змейки превышает заданную
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
            return self.last

    def draw(self):
        """Переопределяем метод draw в классе Snake. Он зарисовывает:
        как выглядит змейка на поле, а также затирает 'след',
        который оставляет наша змейка.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод, отвечающий за сброс змейки на игровом поле.
        В игровом цикле используем для условия:
        'змея врезалась в свое тело'.
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        directions = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(directions)


def main():
    """Основной цикл игры. Сначала создаём экземпляры классов Apple, Snake.
    Вызываем бесконечный цикл, в котором отрисовываются объекты,
    предвигается змейка, проверяет условия, а также обновляет экран.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw()
            apple.draw()
            pygame.display.update()

        pygame.display.update()


if __name__ == '__main__':
    main()
