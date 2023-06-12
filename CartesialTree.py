import time
import random
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

def cartesian_tree(arr):
    if not arr:
        return None
    min_index, min_value = min(enumerate(arr), key=lambda x: x[1])
    root = Node(min_value)
    root.left = cartesian_tree(arr[:min_index])
    root.right = cartesian_tree(arr[min_index + 1:])
    if root.left:
        root.left.parent = root
    if root.right:
        root.right.parent = root
    return root

def search(root, value):
    if not root:
        return False
    if root.value == value:
        return True
    elif value < root.value:
        return search(root.left, value)
    else:
        return search(root.right, value)

def merge(t1, t2):
    if not t1:
        return t2
    if not t2:
        return t1
    if t1.value < t2.value:
        t1.right = merge(t1.right, t2)
        if t1.right:
            t1.right.parent = t1
        return t1
    else:
        t2.left = merge(t1, t2.left)
        if t2.left:
            t2.left.parent = t2
        return t2

def split(root, value):
    if not root:
        return None, None
    if root.value < value:
        low_tree, high_tree = split(root.right, value)
        root.right = low_tree
        if low_tree:
            low_tree.parent = root
        return root, high_tree
    else:
        low_tree, high_tree = split(root.left, value)
        root.left = high_tree
        if high_tree:
            high_tree.parent = root
        return low_tree, root

def insert(root, value):
    t1, t2 = split(root, value)
    new_node = Node(value)
    return merge(merge(t1, new_node), t2)

def delete(root, value):
    t1, t2 = split(root, value)
    if t2.left:
        t2.left.parent = None
    return merge(t1, t2.right)

def printInorder(node):
    if node is None:
        return
    printInorder(node.left)
    print(node.value, end=" ")
    printInorder(node.right)

def printPreorder(node):
    if node is None:
        return
    print(node.value, end=' ')
    printInorder(node.left)
    printInorder(node.right)

def printPostorder(node):
    if node is None:
        return
    printInorder(node.left)
    printInorder(node.right)
    print(node.value, end=' ')

if __name__ == '__main__':
    x, x1, x2, x3, x4, x5, x6, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    b = random.choices(range(10000), k=100000)
    # print(b)

    for i in range(100):
        random.seed(i)
        #a = random.sample(range(2000), 1000)
        #a = random.sample(range(20000), 10000)
        a = random.sample(range(200000), 100000)

        start = time.perf_counter()
        tree = cartesian_tree(a)
        end = time.perf_counter()
        x = x + (end - start)

        start = time.perf_counter()
        printInorder(tree)
        end = time.perf_counter()
        print('\n')
        x1 = x1 + (end - start)

        start = time.perf_counter()
        printPreorder(tree)
        end = time.perf_counter()
        print('\n')
        x2 = x2 + (end - start)

        start = time.perf_counter()
        printPostorder(tree)
        end = time.perf_counter()
        print('\n')
        x3 = x3 + (end - start)

        for j in range(100000):
            start = time.perf_counter()
            insert(tree, b[j])
            end = time.perf_counter()
            x4 = x4 + (end - start)

            start = time.perf_counter()
            search(tree, b[j])
            end = time.perf_counter()
            x5 = x5 + (end - start)

            start = time.perf_counter()
            delete(tree, b[j])
            end = time.perf_counter()
            x6 = x6 + (end - start)

        #s = random.sample(range(2001, 4000), 1000)
        #s = random.sample(range(20001, 40000), 10000)
        s = random.sample(range(200001, 400000), 100000)
        other_tree = cartesian_tree(s)
        start = time.perf_counter()
        merge(tree, other_tree)
        end = time.perf_counter()
        x7 = x7 + (end - start)

        start = time.perf_counter()
        tree1, tree2 = split(tree, 1000)
        end = time.perf_counter()
        x8 = x8 + (end - start)

    #file = open("CartesialTree_1000.txt", "w")
    #file = open("CartesialTree_10000.txt", "w")
    file = open("CartesialTree_100000.txt", "w")
    file.write('Average Running time of the algorithm for creating a tree for a given array:' + '\n')
    file.write(str(x/100) + '\n')
    file.write('Average Running time of the centered tree traversal algorithm:' + '\n')
    file.write(str(x1/100) + '\n')
    file.write('Average Running time of the direct tree traversal algorithm:' + '\n')
    file.write(str(x2/100) + '\n')
    file.write('Average Running time of the reverse tree traversal algorithm:' + '\n')
    file.write(str(x3/100) + '\n')
    file.write('Average Running time of the algorithm for insert an element in the tree:' + '\n')
    file.write(str(x4/100000) + '\n')
    file.write('Average Running time of the algorithm for searching for an element in the tree:' + '\n')
    file.write(str(x5/100000) + '\n')
    file.write('Average Running time of the algorithm for deleting an element in the tree:' + '\n')
    file.write(str(x6/100000) + '\n')
    file.write('Average Running time of the algorithm for merging 2 trees:' + '\n')
    file.write(str(x7/100) + '\n')
    file.write('Average Running time of the algorithm for split operation in the tree:' + '\n')
    file.write(str(x8/100) + '\n')
    file.close()

'''
    #arr = [9, 3, 7, 1, 8, 12, 10, 20, 15, 18, 5]
    #arr = [5, 12, 6, 1, 9]
    arr = [1, 2, 3, 4, 5, 6]
    arr2 = [7, 8, 9]
    tree = cartesian_tree(arr)
    tree2 = cartesian_tree(arr2)
    printInorder(tree)
    print('\n')
    #printInorder(tree2)
    a = merge(tree, tree2)
    print('\n')
    printInorder(a)
    z, z1 = split(tree, 2)
    print('\n')
    printInorder(z)
    print('\n')
    printInorder(z1)
    #insert(tree, 8)
    #print('\n')
    #printInorder(tree)
    #delete(tree, 5)
    #print('\n')
    #printInorder(tree)
    '''
