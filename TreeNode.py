class TreeNode:
    def __init__(self, initial_data):
        self.data = initial_data
        self.children = []
        self.parent = None

    def get_data(self):
        return self.data

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def set_parent(self, parent_node):
        self.parent = parent_node

    def is_leaf(self):
        if len(self.get_children()) == 0:
            return True
        else:
            return False

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.set_parent(self)


    def get_root_distance(self):
        cur_node = self
        i = 0
        while cur_node.parent != None:
            i += 1
            cur_node = cur_node.parent

        return i
        