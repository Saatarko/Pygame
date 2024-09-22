import pygame
pygame.init()

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface((self.width, self.height))  # Создаем поверхность для игрока
        self.surface.fill(self.color)  # Заполняем поверхность цветом
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))  # Создаем Rect на основе surface

    def draw(self, screen):
        screen.blit(self.surface, self.rect)  # Рисуем поверхность на экране

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

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