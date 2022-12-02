from Board import Board
from Tree import Tree
from TreeNode import TreeNode

starting_board = Board(4, 4)

tree = Tree(TreeNode(starting_board))

cur_node = tree.get_root()

print(cur_node.get_children())

for i in range(cur_node.get_data().get_width()):
    if cur_node.get_data().get_top_row()[i].is_empty():
        parent_board = cur_node.get_data()
        new_board = Board(parent_board.get_width(), parent_board.get_height())
        new_board.import_data(parent_board)
        new_board.drop(i)
        cur_node.add_child(TreeNode(new_board))


print(cur_node.get_children())


cur_node = cur_node.get_children()[1]

print(cur_node.get_children())

'''for i in range(cur_node.get_data().get_width()):
    if cur_node.get_data().get_top_row()[i].is_empty():
        parent_board = cur_node.get_data()
        new_board = Board(parent_board.get_width(), parent_board.get_height())
        new_board.import_data(parent_board)
        new_board.drop(i)
        cur_node.add_child(TreeNode(new_board))


print('000000000000000000000000')

for node in cur_node.get_children():
    node.get_data().print_lattice()'''