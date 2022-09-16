from enum import Enum


class Color(Enum):
    RED = 1
    BLACK = 0


class RBNode:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.color = Color.RED


class RBTree:
    def __init__(self):
        self.tree_null = RBNode(0)
        self.tree_null.left_child = None
        self.tree_null.right_child = None
        self.tree_null.color = Color.BLACK
        self.root = self.tree_null

    def rotate_right(self, x):
        y = x.left_child
        x.left_child = y.right_child
        if y.right_child != self.tree_null:
            y.right_child.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right_child:
            x.parent.right_child = y
        else:
            x.parent.left_child = y
        y.right_child = x
        x.parent = y

    def rotate_left(self, x):
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child != self.tree_null:
            y.left_child.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def fix_insert(self, new_node):
        while new_node != self.root and new_node.parent.color == Color.RED:
            if new_node.parent == new_node.parent.parent.right_child:
                uncle = new_node.parent.parent.left_child
                if uncle.color == Color.RED:
                    uncle.color = Color.BLACK
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left_child:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.rotate_left(new_node.parent.parent)
            else:
                uncle = new_node.parent.parent.right_child
                if uncle.color == Color.RED:
                    uncle.color = Color.BLACK
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right_child:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.rotate_right(new_node.parent.parent)
            if new_node == self.root:
                break
        self.root.color = Color.BLACK

    def insert_node(self, val):
        new_node = RBNode(val)
        new_node.parent = None
        new_node.left_child = self.tree_null
        new_node.right_child = self.tree_null
        new_node.color = Color.RED
        parent = None
        curr = self.root
        while curr != self.tree_null:
            parent = curr
            if new_node.val < curr.val:
                curr = curr.left_child
            elif new_node.val > curr.val:
                curr = curr.right_child
            else:
                return
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left_child = new_node
        else:
            parent.right_child = new_node
        if new_node.parent is None:
            new_node.color = Color.BLACK
            return
        if new_node.parent.parent is None:
            return
        self.fix_insert(new_node)

    def fix_deletion(self, x):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left_child:
                s = x.parent.right_child
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.rotate_left(x.parent)
                    s = x.parent.right_child
                if s.left_child.color == Color.BLACK and s.right_child.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right_child.color == Color.BLACK:
                        s.left_child.color = Color.BLACK
                        s.color = Color.RED
                        self.rotate_right(s)
                        s = x.parent.right_child
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right_child.color = Color.BLACK
                    self.rotate_right(x.parent)
                    x = self.root
            else:
                s = x.parent.left_child
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.rotate_right(x.parent)
                    s = x.parent.left_child
                if s.right_child.color == Color.BLACK and s.left_child.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left_child.color == Color.BLACK:
                        s.right_child.color = Color.BLACK
                        s.color = Color.RED
                        self.rotate_left(s)
                        s = x.parent.left_child
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left_child.color = Color.BLACK
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def __rb_transplant(self, a, b):
        if a.parent is None:
            self.root = b
        elif a == a.parent.left_child:
            a.parent.left_child = b
        else:
            a.parent.right_child = b
        b.parent = a.parent

    def minimum(self, node):
        while node.left_child != self.tree_null:
            node = node.left_child
        return node

    def delete_node(self, val):
        node = self.root
        z = self.tree_null
        while node != self.tree_null:
            if node.val == val:
                z = node
            if node.val <= val:
                node = node.right_child
            else:
                node = node.left_child
        if z == self.tree_null:
            print("No node with such value in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left_child == self.tree_null:
            x = z.right_child
            self.__rb_transplant(z, z.right_child)
        elif z.right_child == self.tree_null:
            x = z.left_child
            self.__rb_transplant(z, z.left_child)
        else:
            y = self.minimum(z.right_child)
            y_original_color = y.color
            x = y.right_child
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right_child)
                y.right_child = z.right_child
                y.right_child.parent = y
            self.__rb_transplant(z, y)
            y.left_child = z.left_child
            y.left_child.parent = y
            y.color = z.color
        if y_original_color == Color.BLACK:
            self.fix_deletion(x)

    def __repr__(self):
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)


def print_tree(node, lines, level=0):
    if node.val != 0:
        print_tree(node.left_child, lines, level + 1)
        lines.append('====' * level + '> ' +
                     str(node.val) + ' ' + ('(R)' if node.color == Color.RED else '(B)'))
        print_tree(node.right_child, lines, level + 1)


if __name__ == '__main__':
    red_black = RBTree()

    red_black.insert_node(1)
    red_black.insert_node(11)
    red_black.insert_node(7)
    red_black.insert_node(22)
    red_black.insert_node(34)
    red_black.insert_node(6)
    red_black.insert_node(13)
    print("Red-black tree (horizontally flipped)")
    print(red_black)

    print("\nSame tree, element deleted")
    red_black.delete_node(22)
    print(red_black)
