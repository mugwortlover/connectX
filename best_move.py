from Board import Board
from Tree import Tree
from TreeNode import TreeNode
from display_tree import display_tree

def best_move(starting_board, depth):

    def build_tree_rec(cur_node, depth, current_depth):
        if current_depth < depth:
            #print(current_depth)
            
            for i in range(cur_node.get_data().get_width()):
                if cur_node.get_data().get_top_row()[i].is_empty():
                    parent_board = cur_node.get_data()
                    new_board = Board(parent_board.get_width(), parent_board.get_height())
                    new_board.import_data(parent_board)
                    new_board.drop(i)
                    cur_node.add_child(TreeNode(new_board))

            
            for node in cur_node.get_children():
                build_tree_rec(node, depth, current_depth + 1)
         

    #see the future (create tree)
    tree = Tree(TreeNode(starting_board))
    build_tree_rec(tree.get_root(), depth, 0)

    #if a move win the game, do that
    





    return tree

if __name__ == '__main__':
    from random import randint
    test = Board(4, 4)
    for i in range(7):
        test.drop(randint(0, 3))
    tree = best_move(test, 6)
    display_tree(tree.get_root(), {'x': 'green', 'o': 'blue'}, 0.5, dev_flag=False)
    
    

            

    
