from Board import Board
from Tree import Tree
from TreeNode import TreeNode
from display_tree import display_tree

def best_move(starting_board, depth):

    def build_tree_rec(cur_node, depth, current_depth):
        if current_depth < depth:
            
            for i in range(cur_node.get_data().get_width()):
                if cur_node.get_data().get_top_row()[i].is_empty():
                    parent_board = cur_node.get_data()
                    new_board = Board(parent_board.get_width(), parent_board.get_height())
                    new_board.import_data(parent_board)
                    new_board.drop(i)
                    cur_node.add_child(TreeNode(new_board))

            
            for node in cur_node.get_children():
                build_tree_rec(node, depth, current_depth + 1)
         

    tree = Tree(TreeNode(starting_board))
    build_tree_rec(tree.get_root(), depth, 0)

    display_tree(tree, {'x': 'green', 'o': 'blue'})



if __name__ == '__main__':
    test = Board(10, 10)
    best_move(test, 2)
            

    
