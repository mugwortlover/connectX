from Board import Board
from os import system as sys

def main(win_length):

    board = Board(3, 3)

    switch = True
    while True:
        sys('clear')
        board.print_lattice()
        pos = int(input('pos: '))
        if switch:
            board.drop(pos, 'x')
        else:
            board.drop(pos, 'o')
        switch = not switch

        winner = board.check_winners(win_length)
        if winner != False:
            sys('clear')
            board.print_lattice()
            print(f'{winner} won!')
            break

if __name__ == '__main__':
    main(3)


