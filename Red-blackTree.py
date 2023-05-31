import time

class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1 is red, 0 is black
        self.value = value

class RedBlackTree:
    def __init__(self, use_text_values=False):
        self.nil = Node(None)
        self.nil.color = 0
        self.root = self.nil
        self.use_text_values = use_text_values

    def insert(self, key, value=None):
        node = Node(key, value)
        node.left = self.nil
        node.right = self.nil
        node.parent = None
        node.color = 1

        current = self.root
        parent = None
        while current != self.nil:
            parent = current
            if self.compare(node.key, current.key) < 0:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent == None:
            self.root = node
        elif self.compare(node.key, parent.key) < 0:
            parent.left = node
        else:
            parent.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def delete(self, key):
        node = self.search(key)
        if node == None:
            return

        if node.left == self.nil or node.right == self.nil:
            y = node
        else:
            y = self.tree_successor(node)

        if y.left != self.nil:
            x = y.left
        else:
            x = y.right

        x.parent = y.parent

        if y.parent == None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        if y != node:
            node.key = y.key

        if y.color == 0:
            self.fix_delete(x)

    def search(self, key):
        current = self.root
        while current != self.nil:
            if self.compare(key, current.key) == 0:
                break
            elif self.compare(key, current.key) < 0:
                current = current.left
            else:
                current = current.right

        if current == self.nil:
            return None
        else:
            return current

    def tree_minimum(self, node):
        current = node
        while current.left != self.nil:
            current = current.left
        return current

    def tree_maximum(self, node):
        current = node
        while current.right != self.nil:
            current = current.right
        return current

    def tree_successor(self, node):
        if node.right != self.nil:
            return self.tree_minimum(node.right)

        parent = node.parent
        while parent != None and node == parent.right:
            node = parent
            parent = node.parent
        return parent

    def tree_predecessor(self,node):
        pass

    def fix_insert(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left  # uncle
                if u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right  # uncle

                if u != None and u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)

            if node == self.root:
                break

        self.root.color = 0

    def fix_delete(self, node):
        while node != self.root and node.color == 0:
            if node == node.parent.left:
                w = node.parent.right
                if w.color == 1:
                    w.color = 0
                    node.parent.color = 1
                    self.left_rotate(node.parent)
                    w = node.parent.right

                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    node = node.parent
                elif w.right.color == 0:
                    w.left.color = 0
                    w.color = 1
                    self.right_rotate(w)
                    w = node.parent.right

                w.color = node.parent.color
                node.parent.color = 0
                w.right.color = 0
                self.left_rotate(node.parent)
                node = self.root
            else:
                w = node.parent.left
                if w.color == 1:
                    w.color = 0
                    node.parent.color = 1
                    self.right_rotate(node.parent)
                    w = node.parent.left

                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    node = node.parent
                elif w.left.color == 0:
                    w.right.color = 0
                    w.color = 1
                    self.left_rotate(w)
                    w = node.parent.left

                w.color = node.parent.color
                node.parent.color = 0
                w.left.color = 0
                self.right_rotate(node.parent)
                node = self.root

        node.color = 0

    def left_rotate(self, node):
        y = node.right
        node.right = y.left
        if y.left != self.nil:
            y.left.parent = node

        y.parent = node.parent

        if node.parent == None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y

        y.left = node
        node.parent = y

    def right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != self.nil:
            y.right.parent = node

        y.parent = node.parent

        if node.parent == None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y

        y.right = node
        node.parent = y

    def compare(self, a, b):
        if self.use_text_values:
            if a < b:
                return -1
            if a == b:
                return 0
            if a > b:
                return 1
        else:
            return a - b

    def build_tree(self, arr):
        for i in arr:
            self.insert(i)

    def merge_trees(self, tree):
        arr = tree.to_array()
        self.build_tree(arr)

    def split_tree(self, key):
        new_tree = RedBlackTree(self.use_text_values)
        node = self.search(key)
        if node == None:
            return new_tree

        new_tree.root = node.right
        node.right.parent = None
        node.right = None

        new_tree.fix_insert(node)

        return new_tree

    def intersection(self, tree):
        arr1 = self.to_array()
        arr2 = tree.to_array()
        i = 0
        j = 0
        intersection = []

        while i < len(arr1) and j < len(arr2):
            if arr1[i] == arr2[j]:
                intersection.append(arr1[i])
                i += 1
                j += 1
            elif self.compare(arr1[i], arr2[j]) < 0:
                i += 1
            else:
                j += 1

        new_tree = RedBlackTree(self.use_text_values)
        new_tree.build_tree(intersection)

        return new_tree

    def to_array(self):
        arr = []
        self._to_array(self.root, arr)
        return arr

    def _to_array(self, node, arr):
        if node == None or node == self.nil:
            return

        self._to_array(node.left, arr)
        arr.append(node.key)
        self._to_array(node.right, arr)

    def preorder_traversal(self):
        self._preorder_traversal(self.root)

    def _preorder_traversal(self, node):
        if node == None or node == self.nil:
            return

        print(node.key)
        self._preorder_traversal(node.left)
        self._preorder_traversal(node.right)

    def inorder_traversal(self):
        self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        if node == None or node == self.nil:
            return

        self._inorder_traversal(node.left)
        print(node.key)
        self._inorder_traversal(node.right)

    def postorder_traversal(self):
        self._postorder_traversal(self.root)

    def _postorder_traversal(self, node):
        if node == None or node == self.nil:
            return

        self._postorder_traversal(node.left)
        self._postorder_traversal(node.right)
        print(node.key)

    def find_minimum(self):
        if self.root == None or self.root == self.nil:
            return None

        return self.tree_minimum(self.root).key

    def find_maximum(self):
        if self.root == None or self.root == self.nil:
            return None

        return self.tree_maximum(self.root).key

if __name__ == '__main__':
    rbt = RedBlackTree(use_text_values=True)
    start = time.perf_counter()
    rbt.insert("a", 1)
    end = time.perf_counter()
    print("Время работы алгоритма: ", end - start)
    rbt.insert("b", 2)
    rbt.insert("c", 3)
    node = rbt.search("a")
    print(node.key)
    print()
    rbt.preorder_traversal()
    print()
    rbt.inorder_traversal()
    print()
    rbt.postorder_traversal()