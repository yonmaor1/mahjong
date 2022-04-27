from mahjong import *

deck = getDeck()
hand = getHand(deck)
yon = Player('yon', 0, False)
yon.hand = hand
print(sortHand(yon.hand))
