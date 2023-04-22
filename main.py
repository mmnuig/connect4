
import game

while True:
    game.LoadGame()
    game.RunGame()
    print("Play again? (y/n)", end=' ')
    if input() != 'y':
        break