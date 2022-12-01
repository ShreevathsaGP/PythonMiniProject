# imports
import os
import math
import json
import random
import pygame

pygame.init()
resolution = (600, 400)

# initialize pygame
pygame.init()
pygame.display.set_caption("Algorithm Visualizer")

# window and static background
window = pygame.display.set_mode(resolution)
background = pygame.Surface(resolution)

# colours
white = pygame.Color(240, 240, 240)
black = pygame.Color(0,0,0)
red = pygame.Color(255, 40, 40)
green = pygame.Color(40, 250, 40)

background.fill(black)

check_mask = True

def check_collision(p1, p2, center, radius):
    # circle values: (x - h)^2 + (y - k)^2 = r^2
    h = center[0]
    k = center[1]
    r = radius

    # m = infinite
    if p1[0] == p2[0]:
        higher_y = min(p1[1], p2[1])
        lower_y = max(p1[1], p2[1])

        return ((h - r) <= p1[0] <= (h + r)) and (higher_y <= k <= lower_y)

    # m = 0
    if p1[1] == p2[1]:
        higher_x = max(p1[0], p2[0])
        lower_x = min(p1[0], p2[0])

        return ((k - r) <= p1[1] <= (k + r)) and (lower_x <= h <= higher_x)

    circle_surface = pygame.Surface((2 * r, 2 * r))
    pygame.draw.circle(circle_surface, white, (r, r), r)
    circle_mask = pygame.mask.from_surface(circle_surface)

    # make relative
    # print(p1, p2)
    min_x = min(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    p1 = [p1[0] - min_x, p1[1] - min_y]
    p2 = [p2[0] - min_x, p2[1] - min_y]
    # print(p1, p2)

    line_surface = pygame.Surface((abs(p2[0] - p1[0]), abs(p2[1] - p1[1])))
    pygame.draw.line(line_surface, white, p1, p2)
    line_mask = pygame.mask.from_surface(line_surface)

    cm_pos = (h - r, k - r)
    lm_pos = (min_x, min_y)
    offset = (lm_pos[0] - cm_pos[0], lm_pos[1] - cm_pos[1])

    return (circle_mask.overlap(line_mask, offset) != None)


running = True

line_p1 = [350, 200]
line_p2 = [500, 300]

center = (150, 100)
radius = 30

increment = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # point 1
            if event.key in [pygame.K_w]:
                line_p1[1] -= increment
            
            if event.key in [pygame.K_s]:
                line_p1[1] += increment

            if event.key in [pygame.K_a]:
                line_p1[0] -= increment

            if event.key in [pygame.K_d]:
                line_p1[0] += increment
            # point 1

            # point 2
            if event.key in [pygame.K_UP]:
                line_p2[1] -= increment

            if event.key in [pygame.K_DOWN]:
                line_p2[1] += increment

            if event.key in [pygame.K_LEFT]:
                line_p2[0] -= increment

            if event.key in [pygame.K_RIGHT]:
                line_p2[0] += increment
            # point 2

    window.blit(background, (0,0))

    if check_collision(line_p1, line_p2, center, radius):
        pygame.draw.circle(window, red, center, radius)
    else:
        pygame.draw.circle(window, white, center, radius)

    pygame.draw.line(window, white, tuple(line_p1), tuple(line_p2))

    pygame.display.update()

def check_collision_old(p1, p2, centre, radius):
    # convert into cartesian
    p1 = [p1[0], -1 * p1[1]]
    p2 = [p2[0], -1 * p2[1]]
    centre = [centre[0], -1 * centre[1]]

    # circle values: (x - h)^2 + (y - k)^2 = r^2
    h = centre[0]
    k = centre[1]
    r = radius

    # higher lower
    higher_y = max(p1[1], p2[1])
    lower_y = min(p1[1], p2[1])
    higher_x = max(p1[0], p2[0])
    lower_x = min(p1[0], p2[0])

    # m = infinite
    if p1[0] == p2[0]:
        higher_y = max(p1[1], p2[1])
        lower_y = min(p1[1], p2[1])

        return ((h - r) <= p1[0] <= (h + r)) and (higher_y - r > k > lower_y + r)

    # line values: y = mx + e
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    e = (-1 * m * p1[0]) + p1[1]

    # quadratic equation: [1 + m^2]x^2 + [2m(e - k) - 2h]x + [h^2 + (e - k)^2 - r^2] = 0
    a = 1 + (m ** 2)
    b = (2 * m * (e - k)) - 2 * h
    c = (h ** 2) + ((e - k) ** 2) - (r ** 2)

    # determinant d = b^2 - 4ac
    d = (b ** 2) - (4 * a * c)
    
    return d >= 0 and (lower_x > h - r) and (higher_x) # true if collision
