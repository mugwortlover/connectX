from Node import Node
from os import system as sys

class Board:
    def __init__(self, width, height, turn = 'x'):
        self.width = width
        self.height = height
        self.turn = turn
        self.top_row = self.create_lattice(width, height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_top_left(self):
        return self.top_row[0]

    def get_turn(self):
        return self.turn

    def get_top_row(self):
        return self.top_row
    
    def create_lattice(self, width, height):
        top_list = []

        #populate the top row of nodes
        cur_node = Node()
        top_list.append(cur_node)
        for i in range(width - 1):
            new_node = Node()
            cur_node.right = new_node
            new_node.left = cur_node
            top_list.append(new_node)
            cur_node = new_node

        
        #populate the leftmost column of nodes
        cur_node = top_list[0]
        for i in range(height - 1):
            new_node = Node()
            cur_node.down = new_node
            new_node.up = cur_node
            cur_node = new_node


        #popluate the rest 
        anchor_node = top_list[0].down
        for i in range(height - 1):
            left_node = anchor_node
            top_node = anchor_node.up.right
            for i in range(width - 1):
                new_node = Node()

                left_node.right = new_node
                new_node.left = left_node
                top_node.down = new_node
                new_node.up = top_node

                left_node = left_node.right
                top_node = top_node.right

            anchor_node = anchor_node.down


        return top_list


    def print_lattice(self):
        print('-' * self.width * 2)
        cur_node = self.top_row[0]

        while cur_node != None:
            target_node = cur_node
            txt = ''
            while target_node != None:
                txt += target_node.print_val() + ' '
                target_node = target_node.right
            print(txt)
            cur_node = cur_node.down
        print('-' * self.width * 2)


    def drop(self, pos):
        cur_node = self.top_row[pos]

        if not cur_node.is_empty():
            raise Exception('Illegal move')

        while cur_node.down != None and cur_node.down.is_empty():
            cur_node = cur_node.down

        
        cur_node.set_data(self.turn)

        if self.turn == 'x':
            self.turn = 'o'
        else:
            self.turn = 'x'



    def check_winners(self, length_of_win):

        def contains_all(list):
            value = list[0]
            for val in list[1:]:
                if val != value:
                    return False

            return value

        def scan_list(list, length):
            for index in range(len(list) - length + 1):
                value = contains_all(list[index : index + length])
                if value != False and value != None:
                    return value

            return False
                    


        #check all rows
        anchor_node = self.top_row[0]

        while anchor_node != None:
            cur_node = anchor_node
            row_list = []
            while cur_node != None:
                row_list.append(cur_node.get_data())
                cur_node = cur_node.right
            value = scan_list(row_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.down


        #check all the columns
        anchor_node = self.top_row[0]

        while anchor_node != None:
            cur_node = anchor_node
            col_list = []
            while cur_node != None:
                col_list.append(cur_node.get_data())
                cur_node = cur_node.down
            value = scan_list(col_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.right

        
        #check first half of diagonals (negative slope)
        anchor_node = self.top_row[0]

        while anchor_node != None:
            cur_node = anchor_node
            diag_list = []
            while cur_node != None:
                diag_list.append(cur_node.get_data())
                cur_node = cur_node.right
                if cur_node != None:
                    cur_node = cur_node.down
            value = scan_list(diag_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.right


        anchor_node = self.top_row[0].down

        while anchor_node != None:
            cur_node = anchor_node
            diag_list = []
            while cur_node != None:
                diag_list.append(cur_node.get_data())
                cur_node = cur_node.right
                if cur_node != None:
                    cur_node = cur_node.down
            value = scan_list(diag_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.down


        #check second half of diagonals (positive slope)
        anchor_node = self.top_row[-1]

        while anchor_node != None:
            cur_node = anchor_node
            diag_list = []
            while cur_node != None:
                diag_list.append(cur_node.get_data())
                cur_node = cur_node.left
                if cur_node != None:
                    cur_node = cur_node.down
            value = scan_list(diag_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.left


        anchor_node = self.top_row[-1].down

        while anchor_node != None:
            cur_node = anchor_node
            diag_list = []
            while cur_node != None:
                diag_list.append(cur_node.get_data())
                cur_node = cur_node.left
                if cur_node != None:
                    cur_node = cur_node.down
            value = scan_list(diag_list, length_of_win)
            if value != False:
                return value
            anchor_node = anchor_node.down


        return False

                
    def import_data(self, old_board):
        if self.width != old_board.width or self.height != old_board.height:
            raise ImportError('Board\'s sizes do not match')

        old_anchor_node = old_board.top_row[0]
        anchor_node = self.top_row[0]

        while anchor_node != None:
            copy_node = old_anchor_node
            paste_node = anchor_node
            
            while copy_node != None:
                paste_node.set_data(copy_node.get_data())

                copy_node = copy_node.right
                paste_node = paste_node.right

            old_anchor_node = old_anchor_node.down
            anchor_node = anchor_node.down

        self.turn = old_board.get_turn()


        



if __name__ == '__main__':
    board = Board(7, 6)

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

        winner = board.check_winners(4)
        if winner != False:
            sys('clear')
            board.print_lattice()
            print(f'{winner} won!')
            break

        

    




