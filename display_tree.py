from pgl import GWindow, GLine, GRect, GOval, GCompound, GState, GLabel
from Tree import Tree
from TreeNode import TreeNode
from Board import Board


def display_tree(tree, config_dict):

    def create_arrow_compound(x1, y1, x2, y2, color = 'grey'):
        compound = GCompound()

        line = GLine(x1, y1, x2, y2)
        line.set_color(color)
        compound.add(line)

        '''slope = (y2 - y1)/(x2 - x1)

        arr1 = GLine(x2, y2, )'''

        return compound        

    def create_board_compound(board):
        compound = GCompound()

        #create grid
        for x in range(board.get_width()):
            for y in range(board.get_height()):
                rect = GRect(25, 25)
                compound.add(rect, x * 25, y * 25)

        
        anchor_node = board.get_top_left()
        cur_node = anchor_node

        #populate grid
        while anchor_node != None:
            cur_node = anchor_node
            while cur_node != None:
                if cur_node.get_data() != None:
                    pos = cur_node.get_pos()
                    circle = GOval(15, 15)
                    circle.set_filled(True)

                    if not cur_node.get_data() in config_dict.keys():
                        raise Exception(f'data value {cur_node.get_data()} has no entry in config_dict')

                    circle.set_color(config_dict[cur_node.get_data()])
                    compound.add(circle, pos[0] * 25 + 5, pos[1] * 25 + 5)

                cur_node = cur_node.right
            anchor_node = anchor_node.down

        return compound


    def create_subtree_compound(parent_compound, child_surface_list):
        example_child = child_surface_list[0]
        compound = GCompound()

        #adding bounding rects because GCompound is funny like that
        bounding_rect = GRect(len(child_surface_list) * example_child.get_width() + SPACER * (len(child_surface_list) + 1), 2 * BOARD_PHEIGHT + example_child.get_height())
        bounding_rect.set_color('red')
        #bounding_rect.set_visible(False)  #set this to true to see the bounding rectangles
        compound.add(bounding_rect)


        compound.add(parent_compound, (len(child_surface_list) * example_child.get_width() + SPACER * (len(child_surface_list) + 1)) / 2 - parent_compound.get_width() / 2, 0)


        for i in range(len(child_surface_list)):
            child = child_surface_list[i]
            compound.add(child, SPACER + i * (example_child.get_width() + SPACER), BOARD_PHEIGHT * 2)

            compound.add(create_arrow_compound(parent_compound.get_x() + BOARD_PWIDTH / 2, parent_compound.get_y() + BOARD_PHEIGHT + SPACER / 2, child.get_x() + child.get_width() / 2, child.get_y() - SPACER / 2))

        return compound



    def process_node_rec(node):
        if node.is_leaf():
            return create_board_compound(node.get_data())

        parent = create_board_compound(node.get_data())

        lst = []
        for child_node in node.get_children():
            lst.append(process_node_rec(child_node))

        return create_subtree_compound(parent, lst)


    def drag_handler(e):
        if gs.last_x != None:
            dx, dy = e.get_x() - gs.last_x, e.get_y() - gs.last_y
            if not gs.zoom_mode:
                comp.move(dx, dy)
            else:
                direction = dy / abs(dy)
                comp.scale(1 + direction * 0.1)

        gs.last_x, gs.last_y = e.get_x(), e.get_y()



    def mouseup_handler(e):
        gs.last_x, gs.last_y = None, None


    def key_handler(e):
        key = e.get_key()

        if key == '<SPACE>':
            gs.zoom_mode = not gs.zoom_mode

            if gs.zoom_mode:
                gw.label.set_label('mode: zoom')
            else:
                gw.label.set_label('mode: move')
        




    #constants
    BOARD_PWIDTH = tree.get_root().get_data().get_width() * 25   #board pixel width
    BOARD_PHEIGHT = tree.get_root().get_data().get_height() * 25   #board pixel height
    SPACER = 50  #pixels of whitespace between boards


    
    comp = GCompound()
    comp.add(process_node_rec(tree.get_root()))

    gw = GWindow(2560, 1600)
    gw.add(comp, 0, 0)

    gw.label = GLabel('mode: move')
    gw.label.set_font("bold 10px 'arial'")
    gw.add(gw.label, 5, 5)

    gs = GState()
    gs.last_x, gs.last_y = None, None
    gs.zoom_mode = False

    gw.add_event_listener('drag', drag_handler)
    gw.add_event_listener('mousemove', mouseup_handler)
    #gw.add_event_listener('key', key_handler)


    
   


if __name__ == '__main__':
    pass