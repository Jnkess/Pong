import pygame
import time


def format_time(secs):
    sec = secs % 60
    minute = secs // 60

    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    if sec < 10:
        sec = "0" + str(sec)
    else:
        sec = str(sec)

    mat = minute + ":" + sec

    return mat


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def drawBoard(surface, time=0, leftHeight=200, rightHeight=200, ballx=375, bally=250):
    surface.fill((50, 50, 50))
    draw_rect_alpha(surface, (212, 175, 55, 250), (30, leftHeight, 20, 100))
    draw_rect_alpha(surface, (212, 175, 55, 250), (700, rightHeight, 20, 100))
    for i in range(17):
        pygame.draw.line(surface, (212, 175, 55), (375, i * 30), (375, (i * 30) + 10), 4)
    pygame.draw.circle(surface, (250, 250, 250), (ballx, bally), 10)

    # Draw time
    # draw_rect_alpha(surface, (50, 50, 50, 255), (250, 0, 250, 100))

    fnt = pygame.font.SysFont("roboto", 70)
    mat = format_time(time)
    text = fnt.render(mat, True, (220,220,220))
    surface.blit(text, (310, 0))
    pygame.display.update()


def drawBoard2(surface, time=0, leftHeight=200, rightHeight=200, ballx=375, bally=250):
    surface.fill((50, 50, 50))
    draw_rect_alpha(surface, (212, 175, 55, 250), (30, leftHeight, 20, 100))
    draw_rect_alpha(surface, (212, 175, 55, 250), (700, rightHeight, 20, 100))
    for i in range(17):
        pygame.draw.line(surface, (212, 175, 55), (375, i * 30), (375, (i * 30) + 10), 4)
    pygame.draw.circle(surface, (250, 250, 250), (ballx, bally), 10)

    gameStartFont = pygame.font.SysFont('roboto', 30)
    draw_rect_alpha(surface, (190, 105, 55, 250), (250, 140, 250, 50))
    value = gameStartFont.render("PRESS START TO PLAY", True, (1, 1, 1))
    surface.blit(value, (260, 150))

    draw_rect_alpha(surface, (212, 175, 55, 250), (325, 180, 100, 30))
    value = gameStartFont.render("START", True, (1, 1, 1))
    surface.blit(value, (340, 185))

    # Draw time
    # draw_rect_alpha(surface, (50, 50, 50, 255), (250, 0, 250, 100))
    fnt = pygame.font.SysFont("roboto", 70)
    mat = format_time(time)
    text = fnt.render(mat, True, (220,220,220))
    surface.blit(text, (310, 0))
    pygame.display.update()


def moveBall(ballx, bally, movex, movey):
    ballx = ballx + movex
    bally = bally + movey

    return ballx, bally


def movePaddles(keys, leftHeight, rightHeight):
    # Player on the left
    if keys[pygame.K_w] and leftHeight >= 0:
        leftHeight = leftHeight - 0.35
    if keys[pygame.K_s] and leftHeight <= 400:
        leftHeight = leftHeight + 0.35

    # Player on the rights
    if keys[pygame.K_UP] and rightHeight >= 0:
        rightHeight = rightHeight - 0.35
    if keys[pygame.K_DOWN] and rightHeight <= 400:
        rightHeight = rightHeight + 0.35

    return leftHeight, rightHeight


def collisionWall(bally, bouncey):
    if round(bally) == 0 or round(bally) == 500:
        if bouncey > 0:
            bouncey = bouncey - (2 * bouncey)
        elif bouncey < 0:
            bouncey = bouncey + (2 * abs(bouncey))
    return bouncey


def collisionPaddle(leftHeight, rightHeight, ballx, bally, bouncex, bouncey):
    if round(ballx) == 50:
        if leftHeight - 5 <= round(bally) <= leftHeight + 105:
            tmp = bally - leftHeight
            if tmp >= 60:
                x = 1
                tmp = tmp - 50
            elif tmp <= 40:
                x = -1
                tmp = 50 - tmp
            elif 40 < tmp < 60:
                tmp = -1
                bouncey = bouncey
            if tmp > 50:
                bouncey = bouncey + (x * 0.08)
            elif tmp > 40:
                bouncey = bouncey + (x * 0.065)
            elif tmp > 30:
                bouncey = bouncey + (x * 0.05)
            elif tmp > 20:
                bouncey = bouncey + (x * 0.04)
            elif tmp > 10:
                bouncey = bouncey + (x * 0.03)
            elif tmp >= 0:
                bouncey = bouncey + (x * 0.02)
        else:
            bouncey = 0
        bouncex = bouncex * (-1)

    elif round(ballx) == 700:
        if rightHeight - 5 <= bally <= rightHeight + 105:
            tmp = bally - rightHeight
            if tmp >= 60:
                x = 1
                tmp = tmp - 50
            elif tmp <= 40:
                x = -1
                tmp = 50 - tmp
            elif 40 < tmp < 60:
                tmp = -1
                bouncey = bouncey
            if tmp > 50:
                bouncey = bouncey + (x * 0.08)
            elif tmp > 40:
                bouncey = bouncey + (x * 0.065)
            elif tmp > 30:
                bouncey = bouncey + (x * 0.050)
            elif tmp > 20:
                bouncey = bouncey + (x * 0.04)
            elif tmp > 10:
                bouncey = bouncey + (x * 0.03)
            elif tmp >= 0:
                bouncey = bouncey + (x * 0.02)
        else:
            bouncey = 0
        bouncex = bouncex * (-1)

    return bouncex, bouncey


def checkSpeed(bouncex, bouncey):
    if bouncey > 0.25:
        bouncey = 0.25
    elif bouncey < -0.25:
        bouncey = -0.25

    if bouncex > 2:
        bouncex = 2
    elif bouncex < -2:
        bouncex = -2

    return bouncex, bouncey


def speedIncrease(time, bouncex, x):
    if time % 15 == 0 and time != x:
        if bouncex > 0:
            bouncex = bouncex + 0.1
        if bouncex < 0:
            bouncex = bouncex - 0.1
        x = time
    return bouncex, x


WIDTH, HEIGHT = 750, 500
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
drawBoard(WIN)
pygame.display.update()


def main():
    run = True
    leftH, rightH = 200, 200
    movex = -0.4
    movey = 0.0000000001
    ballx = 375
    bally = 250
    xspeedlvl = 0
    start = time.time()
    play_time = 0
    session = False
    start_time = 3
    begin = 3
    while run:
        while session:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    session = False
                    break

            keys = pygame.key.get_pressed()
            leftH, rightH = movePaddles(keys, leftH, rightH)
            movex, movey = collisionPaddle(leftH, rightH, ballx, bally, movex, movey)
            movey = collisionWall(bally, movey)
            movex, movey = checkSpeed(movex, movey)
            ballx, bally = moveBall(ballx, bally, movex, movey)
            play_time = round(time.time() - start)
            print(play_time)
            drawBoard(WIN, play_time, leftH, rightH, ballx, bally)
            movex, xspeedlvl = speedIncrease(play_time, movex, xspeedlvl)
            print(movex)
            if movey == 0:
                session = False
                break
        while not session and run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    session = True
                    movey = 0
                    break

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if 325 < pos[0] < 425 and 180 < pos[1] < 210:
                        leftH, rightH = 200, 200
                        movex = 0
                        movey = 0
                        ballx = 375
                        bally = 250
                        xspeedlvl = 0
                        begin = 3
                        start_time = 3
                        start = time.time()
                        play_time = 0
                        x = 5
                        drawBoard(WIN, play_time, leftH, rightH, ballx, bally)
                        fnt = pygame.font.SysFont("roboto", 70)
                        text = fnt.render("UWAGA!", True, (255,0,0))
                        WIN.blit(text, (278, 180))
                        pygame.display.update()

                        while start_time > 0:
                            start_time = round(begin - (time.time() - start))
                            print(start_time)
                            print(x)
                            if start_time != x:
                                draw_rect_alpha(WIN, (50, 50, 50, 255), (300, 300, 150, 50))
                                fnt = pygame.font.SysFont("roboto", 70)
                                mat = format_time(start_time)
                                text = fnt.render(mat, True, (255,0,0))
                                WIN.blit(text, (310, 300))
                                pygame.display.update()
                                x = start_time
                        movex = -0.4
                        start = time.time()
                        session = True
                        movey = 0.0000000001
                        break
            drawBoard2(WIN, play_time, leftH, rightH, ballx, bally)


main()
