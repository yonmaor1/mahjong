from player import *
from globals import *
from displays import *
from mahjong import *
pygame.init()

def mouseTime():
    screen = pygame.display.set_mode((WIDTH + SIDEBAR, HEIGHT))
    screen.fill(GREEN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                startTime = time.time()
            if event.type == pygame.MOUSEBUTTONUP:
                endTime = time.time()
                return endTime - startTime


'''screen = pygame.display.set_mode((WIDTH + SIDEBAR, HEIGHT))
deck = getDeck()
players = initPlayers(deck)
giveHands(players, deck)
turn = 0
players[0].name = 'yon'
players[0].won = True
endGame(players, turn, screen)'''



'''deck = getDeck()
for i in range(len(deck) - 1):
    for j in range(i+1, len(deck)):
        if deck[i] is deck[j]:
            print(f'{deck[i]} duplicate')

players = initPlayers('yon')
giveHands(players, deck)

for player in players:
    for i in range(len(player.hand) - 1):
        for j in range(i+1, len(player.hand)):
            if player.hand[i] is player.hand[j]:
                print(f'{player.hand[i]} duplicate')
'''
