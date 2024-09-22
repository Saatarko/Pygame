import pygame
import math

pygame.init()

W = 600
H = 400
sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption('Игра с препятствиями')
pygame.display.set_icon(pygame.image.load("favicon.bmp"))

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60

# Игроки
player_one = True
player_two = False

# Информация о игроках
players = {
    "player_one": {"x": W / 2, "y": 380, "color": BLUE},
    "player_two": {"x": W / 2, "y": 10, "color": GREEN}
}

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

def check_collision_with_obstacles(rect):
    """Проверяем, пересекается ли переданный прямоугольник с любым препятствием"""
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
            # Инициализируем начальные координаты круга (по центру прямоугольника)
            if player_one:
                x_cir = players["player_one"]["x"] + 10  # Центрируем по ширине прямоугольника
                y_cir = players["player_one"]["y"]
            if player_two:
                x_cir = players["player_two"]["x"] + 10  # Центрируем по ширине прямоугольника
                y_cir = players["player_two"]["y"]
            # Координаты точки клика
            x_click, y_click = event.pos

            # Рассчитываем разницу между точкой клика и точкой вылета
            dx = x_click - x_cir
            dy = y_click - y_cir

            # Вычисляем длину вектора (гипотенуза) для нормализации скорости
            length = math.sqrt(dx ** 2 + dy ** 2)

            # Определяем направления по x и y, нормализуя вектор
            x_direction = dx / length
            y_direction = dy / length

            # Создаем объект круга для проверки столкновений
            bullet_rect = pygame.Rect(x_cir - 5, y_cir - 5, 10, 10)
            # Добавляем новый шар в список с учетом цвета и принадлежности игрока
            if not check_collision_with_obstacles(bullet_rect):
                if player_one:
                    color = players["player_one"]["color"]
                if player_two:
                    color = players["player_two"]["color"]
                bullets.append({"x": x_cir, "y": y_cir, "x_dir": x_direction, "y_dir": y_direction, "color": color})

    # Обновляем позицию каждого шарика
    for bullet in bullets[:]:
        bullet["x"] += bullet["x_dir"] * ball_speed
        bullet["y"] += bullet["y_dir"] * ball_speed

        # Создаем объект круга для проверки столкновений
        bullet_rect = pygame.Rect(bullet["x"] - 5, bullet["y"] - 5, 10, 10)

        # Проверяем столкновение шарика с препятствиями
        if check_collision_with_obstacles(bullet_rect):
            bullets.remove(bullet)  # Удаляем шарик, если он сталкивается с препятствием
            continue  # Переходим к следующему шарику

        # Проверяем попадание в другого игрока
        for player_key, player in players.items():
            player_rect = pygame.Rect(player["x"], player["y"], 20, 10)  # Текущая позиция игрока
            if check_bullet_collision(bullet_rect, player_rect):
                if bullet["color"] != (BLUE if player_key == "player_one" else GREEN):  # Проверка цвета
                    if player_key == "player_one":
                        print("Игрок 1 попал в Игрока 2!")
                    else:
                        print("Игрок 2 попал в Игрока 1!")
                    bullets.remove(bullet)  # Удаляем шарик при попадании
                    break

        # Удаляем шарики, которые вышли за пределы экрана
        if bullet["x"] <= 0 or bullet["x"] >= W or bullet["y"] <= 0 or bullet["y"] >= H:
            bullets.remove(bullet)

    # Управление игроками
    keys = pygame.key.get_pressed()

    if player_one:
    # Обновление второго игрока

        new_rect_one = pygame.Rect(players["player_one"]["x"], players["player_one"]["y"], 20, 10)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and players["player_one"]["x"] >= 10:  # Влево
            new_rect_one.x -= speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_one"]["x"] -= speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and players["player_one"]["x"] <= 550:  # Вправо
            new_rect_one.x += speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_one"]["x"] += speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and  players["player_one"]["y"] >= 10:  # Вверх
            new_rect_one.y -= speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_one"]["y"] -= speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and players["player_one"]["y"] <= 380:  # Вниз
            new_rect_one.y += speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_one"]["y"] += speed

    if player_two:

        new_rect_one = pygame.Rect(players["player_two"]["x"], players["player_two"]["y"], 20, 10)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and players["player_two"]["x"] >= 10:  # Влево
            new_rect_one.x -= speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_two"]["x"] -= speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and players["player_two"]["x"] <= 550:  # Вправо
            new_rect_one.x += speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_two"]["x"] += speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and players["player_two"]["y"] >= 10:  # Вверх
            new_rect_one.y -= speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_two"]["y"] -= speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and players["player_two"]["y"] <= 380:  # Вниз
            new_rect_one.y += speed
            if not check_collision_with_obstacles(new_rect_one):
                players["player_two"]["y"] += speed
    # # Обновление второго игрока (пока управляется клавишами по умолчанию)
    # new_rect_two = pygame.Rect(players["player_two"]["x"], players["player_two"]["y"], 45, 10)
    # # Для примера, будем просто двигать второго игрока вниз
    # if players["player_two"]["y"] <= 380:  # Вниз
    #     new_rect_two.y += speed
    #     if not check_collision_with_obstacles(new_rect_two):
    #         players["player_two"]["y"] += speed

    # Рисуем сцену
    sc.fill(WHITE)

    # Рисуем препятствия
    for obstacle in obstacles:
        pygame.draw.rect(sc, RED, obstacle)

    # Рисуем игроков
    for player_key, player in players.items():
        pygame.draw.rect(sc, player["color"], (player["x"], player["y"], 20, 10))

    # Рисуем все шарики
    for bullet in bullets:
        pygame.draw.circle(sc, bullet["color"], (int(bullet["x"]), int(bullet["y"])), 5)

    pygame.display.update()

    clock.tick(FPS)

