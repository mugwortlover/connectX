class Tree:
    def __init__(self, root_node):
        self.root_node = root_node

    def get_height(self):
        #ONLY WORKS ON COMPLETE TREES
        cur_node = self.root_node
        i = 1
        while not cur_node.is_leaf():
            i += 1
            cur_node = cur_node.get_children()[0]

        return i

    def get_root(self):
        return self.root_node

    def layer_to_list(self, layer):
        #for a given layer in the tree, return a list of all that layer's nodes

        if layer > self.get_height():
            raise Exception(f'layer {layer} is invalid')

        lst = []

        def process_node_rec(node):
            if node.get_root_distance() == layer:
                lst.append(node)
            else:
                for node in node.get_children():
                    process_node_rec(node)

        process_node_rec(self.root_node)

        return lst