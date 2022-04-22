from pygame.locals import *
import pygame, random, sys, math, copy, time

WIDTH, HEIGHT = 860, 860
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
