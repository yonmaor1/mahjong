from pygame.locals import *
import pygame, random, sys, math, copy, time

WIDTH, HEIGHT = 860, 860
BOARD = pygame.Rect(0, 0, WIDTH, HEIGHT)
SIDEBAR = 250
SIDEBARRECT = pygame.Rect(WIDTH, 0, SIDEBAR, HEIGHT)
MARGIN = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (73,160,117)
PINK = (255, 194, 194)
MINT = (120, 255, 194)
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
        
    nonSigFigs = len(str(round(step))) # figures before the decimal
    sigFigs = len(str(step)) - nonSigFigs # figures after the decimal
    steps = abs(final - initial) // step

    if final == initial:
        return L
    elif final > initial: 
        direction = 1
    else: 
        direction = -1

    while len(L) <= steps:
        initial += step * direction
        initial = round(initial, sigFigs)
        L.append(initial)

    if direction == 1:
        if L[-1] > final:
            L.pop()
    if direction == -1:
        if L[-1] < final:
            L.pop()
    
    L.append(final)
    return L