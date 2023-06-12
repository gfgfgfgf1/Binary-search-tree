import time
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    # поверните влево
    @staticmethod
    def rotate_left(tree, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            tree.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    # поверните вправо
    @staticmethod
    def rotate_right(tree, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            tree.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    # Splaying operation. Он перемещает element к корневой вершине дерева
    def splay(self, element):
        while element.parent != None:
            if element.parent.parent == None:
                if element == element.parent.left:
                    # zig rotation
                    self.rotate_right(self, element.parent)
                else:
                    # zag rotation
                    self.rotate_left(self, element.parent)
            elif element == element.parent.left and element.parent == element.parent.parent.left:
                # zig-zig rotation
                self.rotate_right(self, element.parent.parent)
                self.rotate_right(self, element.parent)
            elif element == element.parent.right and element.parent == element.parent.parent.right:
                # zag-zag rotation
                self.rotate_left(self, element.parent.parent)
                self.rotate_left(self, element.parent)
            elif element == element.parent.right and element.parent == element.parent.parent.left:
                # zig-zag rotation
                self.rotate_left(self, element.parent)
                self.rotate_right(self, element.parent)
            else:
                # zag-zig rotation
                self.rotate_right(self, element.parent)
                self.rotate_left(self, element.parent)

    def print_preorder_traversal(self, node):
        if node is None:
            return
        print(node.value, end=' ')
        self.print_preorder_traversal(node.left)
        self.print_preorder_traversal(node.right)

    # In-Order traversal
    # Левое поддерево -> Вершина-> Правое поддерево
    def print_inorder_traversal(self, node):
        if node is not None:
            self.print_inorder_traversal(node.left)
            print(node.value, end=' ')
            self.print_inorder_traversal(node.right)

    # Post-Order traversal
    # Левое поддерево -> Правое поддерево -> Вершина
    def print_postorder_traversal(self, node):
        if node is None:
            return
        self.print_postorder_traversal(node.left)
        self.print_postorder_traversal(node.right)
        print(node.value, end=' ')

    # найдите в дереве element
    # и верните соответствующую вершину
    def search_element_on_tree(self, node, element):
        if not node:
            return False
        if node.value == element:
            self.splay(node)
            return True
        elif element < node.value:
            return self.search_element_on_tree(node.left, element)
        else:
            return self.search_element_on_tree(node.right, element)

    # найдите узел с максимальным ключом
    def maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    # функция слияния 2 деревьев
    def merge_trees(self, tree1, tree2):
        if tree1 == None:
            return tree2

        if tree2 == None:
            return tree1

        new_tree = self.maximum(tree1)
        self.splay(new_tree)
        new_tree.right = tree2
        tree2.parent = new_tree
        return new_tree

    # функция разделения дерева на 2 новых дерева
    # дерево tree1 будет содержать элементы меньшие или равные значению element
    # дерево tree2 будет содержать элементы больше значения element
    def split_tree(self, element):
        self.search_element_on_tree(self.root, element)
        if self.root.right != None:
            tree2 = self.root.right
            tree2.parent = None
        else:
            tree2 = None

        tree1 = self.root
        self.root.right = None
        self.root = None
        return tree1, tree2

    # вставить вершину в дереве на соответствующую позицию
    def insert_node(self, element):
        node = Node(element)
        parental_node = None
        new_node = self.root

        while new_node != None:
            parental_node = new_node
            if node.value < new_node.value:
                new_node = new_node.left
            else:
                new_node = new_node.right

        node.parent = parental_node
        if parental_node == None:
            self.root = node
        elif node.value < parental_node.value:
            parental_node.left = node
        else:
            parental_node.right = node
        # splay вершины
        self.splay(node)

    # удалить вершину из дерева
    def delete_node(self, element):
        tree1 = None
        tree2 = None

        # операция разделения
        tree1, tree2 = self.split_tree(element)

        # операция объединениея
        if tree1.left != None:
            tree1.left.parent = None

        self.root = self.merge_trees(tree1.left, tree2)

    def build_tree(self, arr):
        for i in arr:
            self.insert_node(i)

if __name__ == '__main__':
    x, x1, x2, x3, x4, x5, x6, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    b = random.choices(range(10000), k=100000)

    tree = SplayTree()
    a = [1, 2, 3, 4, 5]
    tree.build_tree(a)
    tree.print_inorder_traversal(tree.root)

'''
    for i in range(100):
        random.seed(i)
        #a = random.sample(range(2000), 1000)
        #a = random.sample(range(20000), 10000)
        a = random.sample(range(200000), 100000)

        tree = SplayTree()
        start = time.perf_counter()
        tree.build_tree(a)
        end = time.perf_counter()
        x = x + (end - start)

        start = time.perf_counter()
        tree.print_inorder_traversal(tree.root)
        end = time.perf_counter()
        print('\n')
        x1 = x1 + (end - start)

        start = time.perf_counter()
        tree.print_preorder_traversal(tree.root)
        end = time.perf_counter()
        print('\n')
        x2 = x2 + (end - start)

        start = time.perf_counter()
        tree.print_postorder_traversal(tree.root)
        print('\n')
        end = time.perf_counter()
        x3 = x3 + (end - start)

        for j in range(100000):
            start = time.perf_counter()
            tree.insert_node(b[j])
            end = time.perf_counter()
            x4 = x4 + (end - start)

            start = time.perf_counter()
            find = tree.search_element_on_tree(tree.root, b[j])
            end = time.perf_counter()
            # print(find)
            x5 = x5 + (end - start)

            start = time.perf_counter()
            tree.delete_node(b[j])
            end = time.perf_counter()
            x6 = x6 + (end - start)

        tree2 = SplayTree()
        #s = random.sample(range(2001, 4000), 1000)
        #s = random.sample(range(20001, 40000), 10000)
        s = random.sample(range(200001, 400000), 100000)
        tree2.build_tree(s)
        start = time.perf_counter()
        tree.merge_trees(tree.root, tree2.root)
        end = time.perf_counter()
        x7 = x7 + (end - start)

        start = time.perf_counter()
        new_tree1, new_tree2 = tree.split_tree(b[i])
        end = time.perf_counter()
        #tree.print_inorder_traversal(new_tree1)
        #tree.print_inorder_traversal(new_tree2)
        x8 = x8 + (end - start)

    #file = open("SplayTree_1000.txt", "w")
    #file = open("SplayTree_10000.txt", "w")
    file = open("SplayTree_100000.txt", "w")
    file.write('Average Running time of the algorithm for creating a tree for a given array:' + '\n')
    file.write(str(x / 100) + '\n')
    file.write('Average Running time of the centered tree traversal algorithm:' + '\n')
    file.write(str(x1 / 100) + '\n')
    file.write('Average Running time of the direct tree traversal algorithm:' + '\n')
    file.write(str(x2 / 100) + '\n')
    file.write('Average Running time of the reverse tree traversal algorithm:' + '\n')
    file.write(str(x3 / 100) + '\n')
    file.write('Average Running time of the algorithm for insert an element in the tree:' + '\n')
    file.write(str(x4 / 100000) + '\n')
    file.write('Average Running time of the algorithm for searching for an element in the tree:' + '\n')
    file.write(str(x5 / 100000) + '\n')
    file.write('Average Running time of the algorithm for deleting an element in the tree:' + '\n')
    file.write(str(x6 / 100000) + '\n')
    file.write('Average Running time of the algorithm for merging 2 trees:' + '\n')
    file.write(str(x7 / 100) + '\n')
    file.write('Average Running time of the algorithm for split operation in the tree:' + '\n')
    file.write(str(x8 / 100) + '\n')
    file.close()
'''