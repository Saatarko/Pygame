import pygame
import math

from models import Player, Bullet

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
current_player = None


# Функция для отображения меню
def menu(game_over=False, message = None):
    global current_player


    if game_over:
        show_popup(message)
        game_over=False

    while True:
        sc.fill(WHITE)

        welcome_text = font.render('Добро пожаловать в игру!', True, (0, 0, 0))
        sc.blit(welcome_text, (W // 2 - welcome_text.get_width() // 2, H // 2 - 50))

        # Кнопки выбора игрока
        button_one = font.render('Игрок 1 (Синий)', True, BLUE)
        button_two = font.render('Игрок 2 (Зеленый)', True, GREEN)
        button_three = font.render('Выход', True, RED)
        sc.blit(button_one, (W // 2 - button_one.get_width() // 2, H // 2 + 10))
        sc.blit(button_two, (W // 2 - button_two.get_width() // 2, H // 2 + 50))
        sc.blit(button_three, (W // 2 - button_three.get_width() // 2, H // 2 + 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_one.get_rect(topleft=(W // 2 - button_one.get_width() // 2, H // 2 + 10)).collidepoint(mouse_pos):
                    current_player = "one"

                    return main_game()
                elif button_two.get_rect(topleft=(W // 2 - button_two.get_width() // 2, H // 2 + 50)).collidepoint(mouse_pos):

                    current_player = "two"
                    return main_game()
                elif button_three.get_rect(topleft=(W // 2 - button_three.get_width() // 2, H // 2 + 90)).collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()




def main_game():


    global show_message, current_player
    popup_message = None
    # Флаги для завершения игры
    game_over = False

    player_one_count = player_two_count = 0

    print("current_player", current_player)
    # # Информация о игроках
    # players = {
    #     "player_one": {"x": W / 2, "y": 380, "color": BLUE},
    #     "player_two": {"x": W / 2, "y": 10, "color": GREEN}
    # }

    player_one = Player(W / 2, 380, 20, 10, BLUE)
    player_two = Player(W / 2, 10, 20, 10, GREEN)

    speed = 5
    ball_speed = 5

    # Список для хранения всех выстрелов
    bullets = []


    # Список для хранения всех препятствий
    obstacles = [
        pygame.Rect(250, 200, 80, 20),
        pygame.Rect(100, 200, 80, 20),
        pygame.Rect(400, 200, 80, 20),
        pygame.Rect(150, 100, 80, 20),
        pygame.Rect(350, 300, 80, 20)
    ]

    # Функция проверки столкновения игрока с препятствиями и границами экрана
    def check_collision_with_obstacles_and_bounds(rect):
        """Проверяем, пересекается ли переданный прямоугольник с любым препятствием или выходит за границы экрана"""
        # Проверяем границы экрана
        if rect.left < 0 or rect.right > (W-100) or rect.top < 0 or rect.bottom > H:
            return True

        # Проверяем столкновения с препятствиями
        for obstacle in obstacles:
            if rect.colliderect(obstacle):
                return True

        return False

    def check_bullet_collision(bullet_rect, target_rect):
        """Проверяем, попадает ли пуля в целевой прямоугольник"""
        return bullet_rect.colliderect(target_rect)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Определяем текущие координаты игрока
                if current_player == "one":
                    player_rect = player_one.rect
                elif current_player == "two":
                    player_rect = player_two.rect

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
                if current_player == "one":
                    color_ball = player_one.color
                elif current_player == "two":
                    color_ball = player_two.color

                # Создаем объект пули
                bullet = Bullet(x_cir, y_cir, x_direction, y_direction, color_ball)

                # Проверяем столкновение пули с препятствиями
                if not bullet.check_collision(obstacles):
                    bullets.append(bullet)  # Добавляем пулю в список, если нет коллизии

        # Обновляем позицию каждого шарика
        for bullet in bullets[:]:
            # Перемещение пули
            bullet.move()

            # Проверяем столкновение пули с препятствиями
            if bullet.check_collision(obstacles):
                bullets.remove(bullet)
                continue  # Переходим к следующей пуле

            # Проверяем попадание в другого игрока
            for player in [player_one, player_two]:
                if bullet.rect.colliderect(player.rect):  # Проверяем столкновение пули с rect игрока
                    if bullet.color != player.color:  # Проверка, что пуля другого цвета
                        if player == player_one:
                            print(f"Зеленый игрок попал в Синего! {player_two_count}")
                            player_two_count += 1
                        else:
                            print(f"Синий игрок попал в Зеленого! {player_one_count}")
                            player_one_count += 1
                        bullets.remove(bullet)  # Удаляем пулю при попадании
                        break

            # Удаляем пули, которые вышли за пределы экрана
            if bullet.x <= 0 or bullet.x >= (W - 100) or bullet.y <= 0 or bullet.y >= H:
                bullets.remove(bullet)

        # Управление игроками
        keys = pygame.key.get_pressed()

        if current_player == "one":
            # Обновление второго игрока

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_one.width >= 10:  # Влево
                # Создаем временный rect для проверки столкновения
                new_rect = player_one.rect.move(-speed, 0)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_one.move(-speed, 0)
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_one.width <= 550:  # Вправо
                new_rect = player_one.rect.move(speed, 0)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_one.move(+speed, 0)
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_one.height>= 10:  # Вверх
                new_rect = player_one.rect.move(0, -speed)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_one.move(0, -speed)
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_one.height <= 380:  # Вниз
                new_rect = player_one.rect.move(0, speed)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_one.move(0, speed)

        if current_player == "two":

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_two.width>= 10:  # Влево
                new_rect = player_two.rect.move(-speed, 0)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_two.move(-speed, 0)
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_two.width <= 550:  # Вправо
                new_rect = player_two.rect.move(+speed, 0)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_two.move(+speed, 0)
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_two.height >= 10:  # Вверх
                new_rect = player_two.rect.move(0, -speed)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_two.move(0, -speed)
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_two.height <= 380:  # Вниз
                new_rect = player_two.rect.move(0,speed)
                if not check_collision_with_obstacles_and_bounds(new_rect):
                    player_two.move(0, speed)

        if player_one_count >=5:
            player_one_count = player_two_count = 0
            popup_message = "Игрок 1 выиграл"
            game_over = True
            menu(game_over,popup_message)

        if player_two_count >=5:
            popup_message = "Игрок 2 выиграл"
            game_over = True
            menu(game_over, popup_message)


        # Рисуем сцену
        sc.fill(WHITE)

        # Очищаем поверхность для счета
        surf.fill(WHITE)

        # Рисуем текст на поверхности для счета
        count = font.render('Счет', True, (0, 0, 0))
        player_one_counter = font_count.render(f'Синий:{player_one_count}', True, (0, 0, 0))
        player_two_counter = font_count.render(f'Зеленый:{player_two_count}', True, (0, 0, 0))

        surf.blit(count, (10, 10))
        surf.blit(player_one_counter, (10, 50))
        surf.blit(player_two_counter, (10, 90))

        # Отображаем поверхность счета на основном экране
        sc.blit(surf, (600, 0))

        # Рисуем препятствия
        for obstacle in obstacles:
            pygame.draw.rect(sc, RED, obstacle)

        # Рисуем игроков
        player_one.draw(sc)
        player_two.draw(sc)


        # Рисуем все шарики
        for bullet in bullets:
            bullet.move()
            bullet.draw(sc)
            if bullet.check_collision(obstacles):
                bullets.remove(bullet)




        pygame.display.flip()



        pygame.display.update()

        clock.tick(FPS)

# Вызов меню перед началом игры
menu()