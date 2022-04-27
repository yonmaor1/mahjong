# mahjong
Welcome to Mahjong! This is a single-player AI based mahjong. By default the player plays agains 3 AIs. Graphics are implemented with pygame.

Please run the project by running game.py. You must have pygame installed.

# Issues:
- sometimes tile become same instance of the tile class, and end up occuring in several locations. This was partially fixed by changing the sorting algorithm but it still happen occasionaly
- pygame flashes - I reduced flashing a good bit by using pygame.display.flip() rather then update(), but flashing still occurs
- pass button sometimes doesn't show
