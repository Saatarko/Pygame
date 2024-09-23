import pygame
pygame.init()

# Список для хранения всех препятствий
obstacles = [
    pygame.Rect(250, 200, 80, 20),
    pygame.Rect(100, 200, 80, 20),
    pygame.Rect(400, 200, 80, 20),
    pygame.Rect(150, 100, 80, 20),
    pygame.Rect(350, 300, 80, 20)
]


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
        self.surface = pygame.Surface((self.width, self.height))  # Создаем поверхность для игрока
        self.surface.fill(self.color)  # Заполняем поверхность цветом
        self.rect = (x,y,width,height)  # Создаем Rect на основе surface

    def draw(self, surface):
        pygame.draw.rect(self.surface, self.color, self.rect)  # Рисуем поверхность на экране


    def move(self):

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.width >= 10:
            new_rect = self.rect.move(-self.speed, 0)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.x -= self.speed

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.width <= 550:
            new_rect = self.rect.move(-self.speed, 0)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.x += self.speed

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.height >= 10:
            new_rect = self.rect.move(0, -self.speed)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.y -= self.speed


        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.height <= 380:
            new_rect = self.rect.move(0, self.speed)
            if not self.check_collision_with_obstacles_and_bounds(new_rect):
                self.y += self.speed


        self.update()

        # Функция проверки столкновения игрока с препятствиями и границами экрана

    def check_collision_with_obstacles_and_bounds(self):
        """Проверяем, пересекается ли переданный прямоугольник с любым препятствием или выходит за границы экрана"""
        # Проверяем границы экрана
        if self.rect.left < 0 or self.rect.right > 600 or self.rect.top < 0 or self.rect.bottom > 400:
            return True

        # Проверяем столкновения с препятствиями
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True

        return False

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y, x_dir, y_dir, color, speed=5):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)

    def move(self):
        self.x += self.x_dir * self.speed
        self.y += self.y_dir * self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False