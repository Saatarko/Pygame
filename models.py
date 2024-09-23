import pygame
pygame.init()

# Список для хранения всех препятствий

def get_obstacles():
    return [
        pygame.Rect(250, 200, 80, 20),
        pygame.Rect(100, 200, 80, 20),
        pygame.Rect(400, 200, 80, 20),
        pygame.Rect(150, 100, 80, 20),
        pygame.Rect(350, 300, 80, 20)
    ]

obstacles = get_obstacles()

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
        self.rect = pygame.Rect(x, y, width, height)  # Создаем pygame.Rect

    def draw(self, sc):
        pygame.draw.rect(sc, self.color, self.rect)  # Рисуем поверхность на экране

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            new_rect = self.rect.move(-self.speed, 0)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.x -= self.speed

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            new_rect = self.rect.move(self.speed, 0)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.x += self.speed

        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            new_rect = self.rect.move(0, -self.speed)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.y -= self.speed

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            new_rect = self.rect.move(0, self.speed)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.y += self.speed

        self.update()  # Обновляем pygame.Rect после перемещения

        # Функция проверки столкновения игрока с препятствиями и границами экрана

    def check_collision_with_obstacles_and_bounds(self, new_rect):
        # Проверяем границы экрана
        if new_rect.left < 0 or new_rect.right > 600 or new_rect.top < 0 or new_rect.bottom > 400:
            return True

        # Проверяем столкновения с препятствиями
        for obstacle in obstacles:
            if new_rect.colliderect(obstacle):
                return True

        return False

    def update(self):
        self.rect.topleft = (self.x, self.y)  # Обновляем положение прямоугольника



class Bullet:
    def __init__(self, x, y, x_dir, y_dir, color, speed=5):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)

    # Метод для перемещения пули
    def move(self):
        self.x += self.x_dir * self.speed
        self.y += self.y_dir * self.speed
        self.rect.topleft = (self.x, self.y)

    # Метод для отрисовки пули
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    # Метод для проверки столкновения пули с препятствиями
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False

    # Метод для проверки попадания в игрока
    def check_player_collision(self, players):
        for player in players:
            if self.rect.colliderect(player.rect):
                return player  # Возвращаем игрока, если произошло столкновение
        return None

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "x_dir": self.x_dir,
            "y_dir": self.y_dir,
            "color": self.color,
            "speed": self.speed
        }