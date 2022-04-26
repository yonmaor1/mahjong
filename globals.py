from pygame.locals import *
import pygame, random, sys, math, copy, time

WIDTH, HEIGHT = 860, 860
BOARD = pygame.Rect(0, 0, WIDTH, HEIGHT)
SIDEBAR = 250
MARGIN = 20
WHITE = (255,255,255)
GREEN = (73,160,117)
tileRatio = 44/36
tileTopRatio = 15/36
tileWidth = 40
tileHeight = tileWidth * tileRatio
tileDepth = tileHeight * tileTopRatio
stacksPerSide = 17
tilesPerSide = stacksPerSide * 2
rowLength = stacksPerSide * tileWidth
tilesPerRow = 10
FPS = pygame.time.Clock()

def frange(initial, final, step):
    # float-range: returns a list going from initial to final in step-sized
    # increments
    L = [initial]
    if step == 0:
        return L
        
    steps = abs(final - initial) // step

    if final == initial:
        return L
    elif final > initial: 
        direction = 1
    else: 
        direction = -1

    while len(L) <= steps:
        initial += step * direction
        L.append(initial)

    L.append(final)
    return L