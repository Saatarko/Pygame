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

        # Получение позиции второго игрока
        data_to_send = {
            "position": (player_one.x, player_one.y),
            "bullets": [bullet.__dict__ for bullet in bullets]  # Добавьте все пули текущего игрока
        }
        data = n.send(data_to_send)

        # Убедитесь, что data является словарем
        if isinstance(data, dict):
            player_two_pos = data["position"]
            bullets_for_player_two = data["bullets"]

            player_two.rect.x, player_two.rect.y = player_two_pos

            # Обновление пуль
            bullets_for_player_two = [Bullet(**bullet_data) for bullet_data in bullets_for_player_two]
            bullets.extend(bullets_for_player_two)  # Добавляем пули второго игрока
        else:
            print("Ошибка: получены неверные данные:", data)

        for event in pygame.event.get():



            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Определяем текущие координаты игрока (игрока на клиенте)
                player_rect = player_one.rect

                # Инициализируем начальные координаты пули (по центру прямоугольника игрока)
                x_cir = player_rect.centerx  # Центрируем по ширине
                y_cir = player_rect.centery  # Центрируем по высоте

                # Координаты точки клика
                x_click, y_click = event.pos

                # Рассчитываем разницу между точкой клика и точкой вылета пули
                dx = x_click - x_cir
                dy = y_click - y_cir

                # Вычисляем длину вектора (гипотенуза) для нормализации скорости
                length = math.sqrt(dx ** 2 + dy ** 2)

                # Определяем направления по x и y, нормализуя вектор
                x_direction = dx / length
                y_direction = dy / length

                # Определяем цвет пули в зависимости от игрока
                color_ball = player_one.color  # Цвет пули будет цветом текущего игрока

                # Создаем объект пули
                bullet = Bullet(x_cir, y_cir, x_direction, y_direction, color_ball)

                # Проверяем столкновение пули с препятствиями
                if not bullet.check_collision(obstacles):
                    bullets.append(bullet)  # Добавляем пулю в список, если нет коллизии
                    # Отправка новой пули
                    bullet_data = {
                        "x": bullet.x,
                        "y": bullet.y,
                        "x_dir": bullet.x_dir,
                        "y_dir": bullet.y_dir,
                        "color": bullet.color
                    }
                    n.send({"NEW_BULLET": bullet_data})

        # Обновляем позицию каждого шарика
        for bullet in bullets[:]:
            # Перемещение пули
            bullet.move()

            # Проверяем столкновение пули с препятствиями
            if bullet.check_collision(obstacles):
                bullets.remove(bullet)
                continue  # Переходим к следующей пуле

            # Проверяем попадание в другого игрока
            if bullet.rect.colliderect(player_two.rect):  # Проверяем столкновение с другим игроком
                if bullet.color == player_one.color:  # Если пуля от player_one
                    player_one_score += 1  # Начисляем очки игроку один
                    print(f"Синий игрок попал в Зеленого! Счет Синего: {player_one_score}")
                else:  # Если пуля от player_two
                    player_two_score += 1  # Начисляем очки игроку два
                    print(f"Зеленый игрок попал в Синего! Счет Зеленого: {player_two_score}")
                bullets.remove(bullet)  # Удаляем пулю при попадании
                break

            # Удаляем пули, которые вышли за пределы экрана
            if bullet.x <= 0 or bullet.x >= (W - 100) or bullet.y <= 0 or bullet.y >= H:
                bullets.remove(bullet)

            # Отрисовываем пулю
            bullet.draw(sc)
        #
        # if player_one_score >= 5:
        #     popup_message = "Игрок 1 выиграл"
        #     game_over = True
        #     n.send(f"GAME_OVER:{popup_message}")
        #     # Обнуляем счетчики только после отправки сообщения
        #     player_one_score = player_two_score = 0
        #     menu(game_over, popup_message)
        #
        # if player_two_score >= 5:
        #     popup_message = "Игрок 2 выиграл"
        #     game_over = True
        #     n.send(f"GAME_OVER:{popup_message}")
        #     player_one_score = player_two_score = 0
        #     menu(game_over, popup_message)
        # Управление игроками

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

        for bullet in bullets[:]:
            # рисование пули
            bullet.draw(sc)


        pygame.display.update()

        pygame.display.flip()

        clock.tick(FPS)

# Вызов меню перед началом игры
menu()