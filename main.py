import pygame
import math
import pickle

from network import Network

pygame.init()

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

W = 700
H = 400

surf = pygame.Surface((100,400))
surf.fill(WHITE)

sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption('Игра с препятствиями')
pygame.display.set_icon(pygame.image.load("favicon.bmp"))

sc.blit(surf,(600,0))


# Шрифт
font = pygame.font.Font(None, 36)
font_count= pygame.font.Font(None, 18)

clock = pygame.time.Clock()
FPS = 60


pygame.display.set_caption('Всплывающее сообщение')


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



def show_popup(message, duration=3000):
    """Показать всплывающее сообщение на экране."""
    # Запоминаем текущее время
    text_surface = font.render(message, True, (0, 0, 0))  # Черный текст
    text_rect = text_surface.get_rect(center=(W // 2, H // 2))  # Центрируем текст

    # Очищаем экран и отображаем сообщение
    sc.fill(WHITE)  # Задаем цвет фона, если нужно
    sc.blit(text_surface, text_rect)  # Рисуем текст
    pygame.display.flip()  # Обновляем экран

    # Задержка
    pygame.time.delay(duration)  # Задержка на заданное время



# Переменные для игроков
player_one = False
player_two = False


# Функция для отображения меню
def menu(game_over=False, message = None):

    if game_over:
        show_popup(message)
        game_over=False

    while True:
        sc.fill(WHITE)

        welcome_text = font.render('Добро пожаловать в игру!', True, (0, 0, 0))
        sc.blit(welcome_text, (W // 2 - welcome_text.get_width() // 2, H // 2 - 50))

        # Кнопки выбора игрока
        button_one = font.render('Вход в игру', True, BLUE)
        button_two = font.render('Выход', True, GREEN)
        sc.blit(button_one, (W // 2 - button_one.get_width() // 2, H // 2 + 10))
        sc.blit(button_two, (W // 2 - button_two.get_width() // 2, H // 2 + 50))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_one.get_rect(topleft=(W // 2 - button_one.get_width() // 2, H // 2 + 10)).collidepoint(mouse_pos):
                    return main_game()

                elif button_two.get_rect(topleft=(W // 2 - button_two.get_width() // 2, H // 2 + 50)).collidepoint(mouse_pos):
                    pygame.quit()
                    exit()



        pygame.display.flip()


def main_game():

    global show_message
    popup_message = None
    # Флаги для завершения игры
    game_over = False
    player_one_count = player_two_count = 0

    # Соединение с сервером
    n = Network()

    # Получаем начальные позиции игроков от сервера
    player_one_pos = n.getPos()
    player_two_pos = n.getPos()

    # Создаем игроков на основе полученных координат
    player_one = Player(player_one_pos[0], player_one_pos[1], 20, 10, BLUE)
    player_two = Player(player_two_pos[0], player_two_pos[1], 20, 10, GREEN)



    while True:

        # Получение позиции второго игрока
        player_two_pos = n.send((player_one.x, player_one.y))
        player_two.rect.x, player_two.rect.y = player_two_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Управление игроками

        player_one.move()


        # Рисуем сцену
        sc.fill(WHITE)

        # Очищаем поверхность для счета
        surf.fill(WHITE)


        # Рисуем препятствия
        for obstacle in obstacles:
            pygame.draw.rect(sc, RED, obstacle)

        player_one.draw(sc)
        player_two.draw(sc)

        pygame.display.update()

        pygame.display.flip()

        clock.tick(FPS)

# Вызов меню перед началом игры
menu()