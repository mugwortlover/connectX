from pgl import GWindow, GLine, GRect, GOval, GCompound, GState, GLabel, GPoint
from Tree import Tree
from TreeNode import TreeNode
from Board import Board
import math


def display_tree(root_node, config_dict, initial_scale_factor = 1.0, dev_flag = False):
    '''
    function to graphically display the connectX tree of possibilities

    @root_node (TreeNode): root node of tree
    @config_dict (dict): dict matching the boards' data values to colors 
        ex. if the boards contained data values ('x', 'o') then {'x': 'red', 'o': 'blue'} would match 'x' to red and 'o' to blue
    @initial_scale_factor (float): initial scale factor. Default: 1.0
    @dev_flag (bool): used for development. shows bounding boxes for subtree compounds and global center lines. Default: False
    '''

    def create_arrow_compound(x1, y1, x2, y2, color = 'grey'):
        #create a compound for connecting arrows
        compound = GCompound()

        line = GLine(x1, y1, x2, y2)
        line.set_color(color)
        compound.add(line)

        '''slope = (y2 - y1)/(x2 - x1)

        arr1 = GLine(x2, y2, )'''

        return compound        

    def create_board_compound(board):
        #create a GCompound for one board

        nonlocal scale_factor
        compound = GCompound()

        #create grid
        for x in range(board.get_width()):
            for y in range(board.get_height()):
                rect = GRect(25 * scale_factor, 25 * scale_factor)
                compound.add(rect, x * 25 * scale_factor, y * 25 * scale_factor)

        
        anchor_node = board.get_top_left()
        cur_node = anchor_node

        #populate grid
        while anchor_node != None:
            cur_node = anchor_node
            while cur_node != None:
                if cur_node.get_data() != None:
                    pos = cur_node.get_pos()
                    circle = GOval(15 * scale_factor, 15 * scale_factor)
                    circle.set_filled(True)

                    if not cur_node.get_data() in config_dict.keys():
                        raise Exception(f'data value {cur_node.get_data()} has no entry in config_dict')

                    circle.set_color(config_dict[cur_node.get_data()])
                    compound.add(circle, (pos[0] * 25 + 5) * scale_factor, (pos[1] * 25 + 5) * scale_factor)

                cur_node = cur_node.right
            anchor_node = anchor_node.down

        return compound


    def create_subtree_compound(parent_compound, child_surface_list):
        #creates a GCompound that inclues a parent compound (a single Board compound) and its child compounds
        example_child = child_surface_list[0]
        compound = GCompound()

        #adding bounding rects because GCompound is funny like that
        bounding_rect = GRect(len(child_surface_list) * example_child.get_width() + SPACER * (len(child_surface_list) + 1), 2 * BOARD_PHEIGHT + example_child.get_height())
        if dev_flag:
            bounding_rect.set_color('red')
        else:
            bounding_rect.set_color('white')
        compound.add(bounding_rect)


        compound.add(parent_compound, (len(child_surface_list) * example_child.get_width() + SPACER * (len(child_surface_list) + 1)) / 2 - parent_compound.get_width() / 2, 0)


        for i in range(len(child_surface_list)):
            child = child_surface_list[i]
            compound.add(child, SPACER + i * (example_child.get_width() + SPACER), BOARD_PHEIGHT * 2)

            compound.add(create_arrow_compound(parent_compound.get_x() + BOARD_PWIDTH / 2, parent_compound.get_y() + BOARD_PHEIGHT + SPACER / 2, child.get_x() + child.get_width() / 2, child.get_y() - SPACER / 2))

        return compound



    def process_node_rec(node):
        #recursively process all nodes to create tree
        if node.is_leaf():
            return create_board_compound(node.get_data())

        parent = create_board_compound(node.get_data())

        lst = []
        for child_node in node.get_children():
            lst.append(process_node_rec(child_node))

        return create_subtree_compound(parent, lst)


    def drag_handler(e):
        #callback function for mouse drag
        if gs.last_x != None:
            dx, dy = e.get_x() - gs.last_x, e.get_y() - gs.last_y
            gw.comp.move(dx, dy)
            point = gw.comp.get_location()
            gs.comp_location = (point.get_x(), point.get_y())
            
                    
        gs.last_x, gs.last_y = e.get_x(), e.get_y()



    def mouseup_handler(e):
        #callback function for the end of mouse drag
        gs.last_x, gs.last_y = None, None


    def key_handler(e):
        #callback function for keys
        nonlocal scale_factor
        key = e.get_key()

        if key == 'a':
            scale_factor += 0.1
            main_display()
            #gw.comp.move(gw.comp.get_width() / 2, gw.comp.get_height() / 2)

        elif key == 's':
            scale_factor -= 0.1
            main_display()
            #gw.comp.move(gw.comp.get_width() * 0.1 / 2, gw.comp.get_height() * 0.1 / 2)
           


    def main_display():
        #display the objects on the GWindow

        #update distance constants to match new scale factor
        nonlocal BOARD_PWIDTH, BOARD_PHEIGHT, SPACER, scale_factor
        BOARD_PWIDTH = root_node.get_data().get_width() * 25 * scale_factor   #board pixel width
        BOARD_PHEIGHT = root_node.get_data().get_height() * 25 * scale_factor   #board pixel height
        SPACER = 50 * scale_factor   #pixels of whitespace between boards

        if gw.comp != None:
            gw.remove(gw.comp)
        if gw.label != None:
            gw.remove(gw.label)

        #graphical tree
        gw.comp = process_node_rec(root_node)
        x, y = gs.comp_location[0], gs.comp_location[1]
        gw.add(gw.comp, x, y)

        #label
        gw.label = GLabel(f'zoom: {round(scale_factor, 1)}X')
        gw.label.set_font("bold 10px 'arial'")
        gw.add(gw.label, 10, 10)

        



    #constants
    scale_factor = initial_scale_factor
    BOARD_PWIDTH = root_node.get_data().get_width() * 25 * scale_factor   #board pixel width
    BOARD_PHEIGHT = root_node.get_data().get_height() * 25 * scale_factor   #board pixel height
    SPACER = 50 * scale_factor #pixels of whitespace between boards

    #initialize GWindow, GState, and listeners
    gw = GWindow(2560 / 2, 1600 / 2)
    gw.comp = None
    gw.label = None
    
    gs = GState()
    gs.last_x, gs.last_y = None, None
    gs.comp_location = (0, 0)

    main_display()

    gw.add_event_listener('drag', drag_handler)
    gw.add_event_listener('mouseup', mouseup_handler)
    gw.add_event_listener('key', key_handler)

    if dev_flag:
        line1 = GLine(gw.get_width() / 2, 0, gw.get_width() / 2, gw.get_height())
        line1.set_color('red')
        gw.add(line1)

        line2 = GLine(0, gw.get_height() / 2, gw.get_width(), gw.get_height() / 2)
        line2.set_color('red')
        gw.add(line2)




    
   


if __name__ == '__main__':
    pass