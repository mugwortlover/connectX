class Node:
    def __init__(self, initial_value = None):
        self.data = initial_value
        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def print_val(self):
        if self.data == None:
            return '-'
        else:
            return f'{self.data}'


    def is_empty(self):
        if self.data == None:
            return True
        else:
            return False


    def set_data(self, val):
        self.data = val
        

    def get_data(self):
        return self.data