import sys
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def __print_helper(self, currPtr, indent, last):
        # выведите древовидную структуру на экран
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            print(currPtr.data)

            self.__print_helper(currPtr.left, indent, False)
            self.__print_helper(currPtr.right, indent, True)

    def __search_tree_helper(self, node, key):
        if node == None or key == node.data:
            return node

        if key < node.data:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)

    def __delete_node_helper(self, node, key):
        x = None
        t = None
        s = None
        while node != None:
            if node.data == key:
                x = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if x == None:
            print
            "Couldn't find key in the tree"
            return

        # операция разделения
        self.__splay(x)
        if x.right != None:
            t = x.right
            t.parent = None
        else:
            t = None

        s = x
        s.right = None
        x = None

        # операция объединениея
        if s.left != None:
            s.left.parent = None

        self.root = self.__join(s.left, t)
        s = None

    # поверните влево
    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # поверните вправо
    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x

        y.parent = x.parent;
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # Splaying operation. Он перемещает x к корневой вершине дерева
    def __splay(self, x):
        while x.parent != None:
            if x.parent.parent == None:
                if x == x.parent.left:
                    # zig rotation
                    self.__right_rotate(x.parent)
                else:
                    # zag rotation
                    self.__left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.__right_rotate(x.parent.parent)
                self.__right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.__left_rotate(x.parent.parent)
                self.__left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.__left_rotate(x.parent)
                self.__right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.__right_rotate(x.parent)
                self.__left_rotate(x.parent)

    # соединяет два дерева s и t
    def __join(self, s, t):
        if s == None:
            return t

        if t == None:
            return s

        x = self.maximum(s)
        self.__splay(x)
        x.right = t
        t.parent = x
        return x

    def __pre_order_helper(self, node):
        if node != None:
            sys.stdout.write(node.data + " ")
            self.__pre_order_helper(node.left)
            self.__pre_order_helper(node.right)

    def __in_order_helper(self, node):
        if node != None:
            self.__in_order_helper(node.left)
            sys.stdout.write(node.data + " ")
            self.__in_order_helper(node.right)

    def __post_order_helper(self, node):
        if node != None:
            self.__post_order_helper(node.left)
            self.__post_order_helper(node.right)
            sys.std.out.write(node.data + " ")

    # Pre-Order traversal
    # Вершина->Левое поддерево->Правое поддерево
    def preorder(self):
        self.__pre_order_helper(self.root)

    # In-Order traversal
    # Левое поддерево -> Вершина-> Правое поддерево
    def inorder(self):
        self.__in_order_helper(self.root)

    # Post-Order traversal
    # Левое поддерево -> Правое поддерево -> Вершина
    def postorder(self):
        self.__post_order_helper(self.root)

    # найдите в дереве ключ k
    # и верните соответствующую вершину
    def search_tree(self, k):
        x = self.__search_tree_helper(self.root, k)
        if x != None:
            self.__splay(x)

    # найдите узел с максимальным ключом
    def minimum(self, node):
        while node.left != None:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    # найдите преемника данного узла
    def successor(self, x):
        # если правое поддерево не равно null,
        # преемником является крайняя левая вершина в
        # правом поддереве
        if x.right != None:
            return self.minimum(x.right)

        # else это самый младший предок x, чья
        # левая дочерняя вершина также является предком x.
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

    # найти предшественника указанной вершины
    def predecessor(self, x):
        # если левое поддерево не равно null,
        # предшественником является самая правая вершина в
        # левом поддереве
        if x.left != None:
            return self.maximum(x.left)

        y = x.parent
        while y != None and x == y.left:
            x = y
            y = y.parent
        return y

    # вставить вершину в дереве на соответствующую позицию
    def insert(self, key):
        node = Node(key)
        y = None
        x = self.root

        while x != None:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y это родительская вершина x
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node
        # splay вершины
        self.__splay(node)

    # удалить вершину из дерева
    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)

    # вывести древовидную структуру на экран
    def pretty_print(self):
        self.__print_helper(self.root, "", True)


if __name__ == '__main__':
    tree = SplayTree()
    start = time.perf_counter()
    tree.insert(33)
    end = time.perf_counter()
    print("Время работы алгоритма: ", end - start)
    tree.insert(44)
    tree.insert(67)
    tree.insert(5)
    tree.insert(89)
    tree.insert(41)
    tree.insert(98)
    tree.insert(1)
    tree.pretty_print()
    tree.search_tree(33)
    tree.search_tree(44)
    tree.pretty_print()
    tree.delete_node(89)
    tree.delete_node(67)
    tree.delete_node(41)
    tree.delete_node(5)
    tree.pretty_print()
    tree.delete_node(98)
    tree.delete_node(1)
    tree.delete_node(44)
    tree.delete_node(33)
    tree.pretty_print()