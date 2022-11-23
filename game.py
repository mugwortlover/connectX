from Board import Board
from os import system as sys

def main(win_length):

    board = Board(5, 5)

    while True:
        sys('clear')
        board.print_lattice()
        pos = int(input('pos: '))
        board.drop(pos)

        winner = board.check_winners(win_length)
        if winner != False:
            sys('clear')
            board.print_lattice()
            print(f'{winner} won!')
            break

if __name__ == '__main__':
    main(4)


