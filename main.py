import pygame
import math
import pickle

from network import Network
from models import Player, Bullet

pygame.init()

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

W = 700
H = 400

obstacles = [
    pygame.Rect(250, 200, 80, 20),
    pygame.Rect(100, 200, 80, 20),
    pygame.Rect(400, 200, 80, 20),
    pygame.Rect(150, 100, 80, 20),
    pygame.Rect(350, 300, 80, 20)
]

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

# Список для хранения пуль
bullets = []
bullets2 = []

# Функция для отображения меню
def menu(game_over=False, message = None):

    if game_over:
        show_popup(message)
        game_over=False

    while True:

        sc.fill(WHITE)
        welcome_text = font.render('Добро пожаловать в игру - мочилово!', True, (0, 0, 0))
        sc.blit(welcome_text, (W // 2 - welcome_text.get_width() // 2, H // 2 - 50))

        # Кнопки выбора игрока
        button_one_text = font.render('Вход в игру', True, BLUE)
        button_two_text = font.render('Выход', True, GREEN)

        # Определяем прямоугольники для кнопок
        button_one_rect = button_one_text.get_rect(center=(W // 2, H // 2 + 10))
        button_two_rect = button_two_text.get_rect(center=(W // 2, H // 2 + 50))

        # Отображаем текст кнопок
        sc.blit(button_one_text, button_one_rect.topleft)
        sc.blit(button_two_text, button_two_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_one_rect.collidepoint(mouse_pos):
                    return main_game()

                elif button_two_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()


def main_game():

    global bullets_for_player_two
    player_one_score = player_two_score = 0

    # Соединение с сервером
    n = Network()

    # Получаем начальные позиции игроков от сервера
    player_one_pos = n.getPos()
    player_two_pos = n.getPos()

    # Создаем игроков на основе полученных координат
    player_one = Player(player_one_pos[0], player_one_pos[1], 20, 10, BLUE)
    player_two = Player(player_two_pos[0], player_two_pos[1], 20, 10, GREEN)


    while True:

        data_to_send = {
            "position": (player_one.x, player_one.y),
            # Теперь пули на стороне клиента отправлять не нужно, их будет обрабатывать сервер
        }
        data = n.send(data_to_send)

        # Проверка и обработка полученных данных
        if isinstance(data, dict):

            if "game_over" in data and data["game_over"]:
                # Обработка конца игры
                menu(game_over=True,message=data["message"])
                print(data["message"])  # Вывод сообщения о конце игры
                # Здесь можно вызвать функцию для завершения игры или показать сообщение
            else:
                # Обработка обновлений для второго игрока и пуль
                player_two_pos = data["position"]
                # bullets_for_player_two = data["bullets"]

                if "count" in data:
                    player_one_score, player_two_score = data["count"]

            # Обновляем позицию второго игрока
            player_two.rect.x, player_two.rect.y = player_two_pos

            # Очищаем локальный список пуль и обновляем его

            bullets.clear()  # Очищаем старые пули
            bullets.extend([Bullet(bullet_data["x"], bullet_data["y"], bullet_data["x_dir"], bullet_data["y_dir"], BLUE) for bullet_data in data["bullets"]])

            # Очищаем локальный список пуль для второго игрока
            bullets2.clear()  # Очищаем старые пули
            bullets2.extend([Bullet(bullet_data["x"], bullet_data["y"], bullet_data["x_dir"], bullet_data["y_dir"], GREEN) for bullet_data in data["bullets2"]])

        for event in pygame.event.get():



            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Определяем текущие координаты игрока
                player_rect = player_one.rect

                # Начальные координаты пули (по центру прямоугольника игрока)
                x_cir = player_rect.centerx
                y_cir = player_rect.centery

                # Координаты точки клика
                x_click, y_click = event.pos

                # Рассчитываем разницу между точкой клика и точкой вылета пули
                dx = x_click - x_cir
                dy = y_click - y_cir

                # Вычисляем длину вектора для нормализации
                length = math.sqrt(dx ** 2 + dy ** 2)

                # Определяем направления по x и y
                x_direction = dx / length
                y_direction = dy / length

                # Определяем цвет пули
                color_ball = player_one.color

                # Создаем объект пули
                bullet = Bullet(x_cir, y_cir, x_direction, y_direction, color_ball)

                # Проверяем столкновение пули с препятствиями
                if not bullet.check_collision(obstacles):
                    bullets.append(bullet)  # Добавляем пулю в список
                    # Отправка новой пули с использованием метода serialize
                    n.send({"NEW_BULLET": bullet.serialize()})

        player_one.move()

        # Рисуем сцену
        sc.fill(WHITE)

        # Очищаем поверхность для счета
        surf.fill(WHITE)

        # Рисуем текст на поверхности для счета
        count = font.render('Счет', True, (0, 0, 0))
        player_one_counter = font_count.render(f'Синий:{player_one_score}', True, (0, 0, 0))
        player_two_counter = font_count.render(f'Зеленый:{player_two_score}', True, (0, 0, 0))

        surf.blit(count, (10, 10))
        surf.blit(player_one_counter, (10, 50))
        surf.blit(player_two_counter, (10, 90))

        # Отображаем поверхность счета на основном экране
        sc.blit(surf, (600, 0))

        # Рисуем препятствия
        for obstacle in obstacles:
            pygame.draw.rect(sc, RED, obstacle)

        player_one.draw(sc)
        player_two.draw(sc)

        for bullet in bullets:
            bullet.draw(sc)
        for bullet in bullets2:
            bullet.draw(sc)

        pygame.display.update()

        pygame.display.flip()

        clock.tick(FPS)

# Вызов меню перед началом игры
menu()