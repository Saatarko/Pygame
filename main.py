import pygame

pygame.init()

W = 600
H = 400
sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption('Еще одна попытка сделать пинг-понг')
pygame.display.set_icon(pygame.image.load("favicon.bmp"))


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)

clock =  pygame.time.Clock()
FPS = 60

x = W/2
y = 380
speed = 5
speed_cir = 1


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_cir = x
                y_cir = y
                cir = pygame.draw.circle(sc, RED, (x_cir, y_cir), 5)

    if cir !=0:
        y_cir -=speed_cir
        if y_cir<=0:
            del cir

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -=speed
    elif keys[pygame.K_RIGHT]:
        x +=speed

    sc.fill(WHITE)
    pygame.draw.rect(sc,BLUE,(x,y,45, 10))
    pygame.display.update()

    clock.tick(FPS)






     # колхозный метод проверки нажатости кнопко
    # mleft = mright = False
    # #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             mleft = True
    #         elif event.key == pygame.K_RIGHT:
    #             mright = True
    #     elif event.type == pygame.KEYUP:
    #         if event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
    #             mleft = mright = False
    #
    # if mright:
    #     x +=speed
    # elif mleft:
    #     x -=speed