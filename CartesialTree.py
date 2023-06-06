import time
import random
class Node:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None

class CartesianSearchTree:
	def __init__(self, data_type):
		self.root = None
		self.data_type = data_type

	def insert(self, value):
		if not self.root:
			self.root = Node(value)
		else:
			self._insert(value, self.root)

	def _insert(self, value, node):
		if value < node.value:
			if not node.left:
				node.left = Node(value)
			else:
				self._insert(value, node.left)
		elif value >= node.value:
			if not node.right:
				node.right = Node(value)
			else:
				self._insert(value, node.right)

	def find(self, value):
		current_node = self.root
		while current_node is not None:
			if value == current_node.value:
				return True
			elif value < current_node.value:
				current_node = current_node.left
			else:
				current_node = current_node.right
		return False

	def delete(self, val):
		# Base Case
		if self.root is None:
			return

		# Find the node to be deleted
		temp = self.root
		parent = None
		while temp is not None and temp.value != val:
			parent = temp
			if val < temp.value:
				temp = temp.left
			else:
				temp = temp.right

			# If node to be deleted is not found
		if temp is None:
			return

		# If node to be deleted has one child
		if temp.left is None:
			if parent is None:
				self.root = temp.right
			elif temp is parent.left:
				parent.left = temp.right
			else:
				parent.right = temp.right

			# If node to be deleted has two children
		elif temp.right is None:
			if parent is None:
				self.root = temp.left
			elif temp is parent.left:
				parent.left = temp.left
			else:
				parent.right = temp.left

			# If node to be deleted has two children
		else:
			successor = temp.right
			while successor.left is not None:
				successor = successor.left
			temp.value = successor.value
			if successor is temp.right:
				temp.right = successor.right
			else:
				temp.left = successor.right

	def build_from_array(self, arr):
		for i in arr:
			self.insert(i)

	def merge(self, other_tree):
		if self.root is None:
			self.root = other_tree.root
			return
		elif other_tree.root is None:
			return

		if self.data_type == 'numeric':
			curr = self.root

			while curr.right is not None:
				curr = curr.right

			while other_tree.root is not None:
				self.insert(other_tree.root.value)
				other_tree.delete(other_tree.root.value)

		else:
			words = other_tree.root.value.split(' ')
			curr = self.root

			while curr.right is not None and curr.right.value.split(' ')[0] > words[0]:
				curr = curr.right

			while other_tree.root is not None:
				self.insert(other_tree.root.value)
				other_tree.delete(other_tree.root.value)

	def split(self, value):
		new_tree = CartesianSearchTree(self.data_type)

		if self.data_type == 'numeric':
			curr = self.root

			while curr is not None and curr.value != value:
				if value < curr.value:
					curr = curr.left
				else:
					curr = curr.right

			if curr is None:
				return new_tree

			new_tree.root = curr.right
			if curr.right is not None:
				curr.right.parent = None
				curr.right = None

		else:
			words = value.split(' ')
			curr = self.root

			while curr is not None and curr.value.split(' ')[0] != words[0]:
				if words[0] < curr.value.split(' ')[0]:
					curr = curr.left
				else:
					curr = curr.right

			if curr is None:
				return new_tree

			new_tree.root = curr.right
			if curr.right is not None:
				curr.right.parent = None
			curr.right = None

		return new_tree

	def intersection(self, other_tree):
		result_tree = CartesianSearchTree(self.data_type)

		if self.root is None or other_tree.root is None:
			return result_tree

		if self.data_type == 'numeric':
			curr1 = self.root
			curr2 = other_tree.root

		while curr1 is not None and curr2 is not None:
			if curr1.value == curr2.value:
				result_tree.insert(curr1.value)
				curr1 = curr1.left
				curr2 = curr2.left
			elif curr1.value < curr2.value:
				curr1 = curr1.right
			else:
				curr2 = curr2.right

		else:
			curr1 = self.root
			curr2 = other_tree.root

			while curr1 is not None and curr2 is not None:
				if curr1.value.split(' ')[0] == curr2.value.split(' ')[0]:
					result_tree.insert(curr1.value)
					curr1 = curr1.left
					curr2 = curr2.left
				elif curr1.value.split(' ')[0] < curr2.value.split(' ')[0]:
					curr1 = curr1.right
				else:
					curr2 = curr2.right

		return result_tree

	def preorder_traversal(self, node):
		if node is not None:
			print(node.value, end = ' ')
			self.preorder_traversal(node.left)
			self.preorder_traversal(node.right)

	def inorder_traversal(self, node):
		if node is not None:
			self.inorder_traversal(node.left)
			print(node.value, end = ' ')
			self.inorder_traversal(node.right)

	def postorder_traversal(self, node):
		if node is not None:
			self.postorder_traversal(node.left)
			self.postorder_traversal(node.right)
			print(node.value, end = ' ')

	def get_minimum(self):
		if self.root is None:
			return None

		curr = self.root
		while curr.left is not None:
			curr = curr.left

		return curr.value

	def get_maximum(self):
		if self.root is None:
			return None

		curr = self.root
		while curr.right is not None:
			curr = curr.right

		return curr.value


if __name__ == '__main__':
	tree = CartesianSearchTree('numeric')
	x, x1, x2, x3, x4, x5, x6, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0, 0
	b = random.choices(range(10000), k=100000)
	#print(b)

	for i in range(100):
		random.seed(i)
		#a = random.sample(range(10000), 1000)
		a = random.sample(range(20000), 10000)
		#a = random.sample(range(200000), 100000)

		start = time.perf_counter()
		tree.build_from_array(a)
		end = time.perf_counter()
		x = x + (end - start)

		start = time.perf_counter()
		tree.inorder_traversal(tree.root)
		end = time.perf_counter()
		x1 = x1 + (end - start)

		start = time.perf_counter()
		tree.preorder_traversal(tree.root)
		end = time.perf_counter()
		x2 = x2 + (end - start)

		start = time.perf_counter()
		tree.postorder_traversal(tree.root)
		end = time.perf_counter()
		x3 = x3 + (end - start)

		for j in range(100000):
			start = time.perf_counter()
			tree.insert(b[j])
			end = time.perf_counter()
			x4 = x4 + (end - start)

			start = time.perf_counter()
			tree.find(b[j])
			end = time.perf_counter()
			# if tree.find(b[j]):
			#	print("Value is in tree")
			# else:
			#	print("Value is not in tree")
			x5 = x5 + (end - start)

			start = time.perf_counter()
			tree.delete(b[j])
			end = time.perf_counter()
			x6 = x6 + (end - start)

		other_tree = CartesianSearchTree('numeric')
		other_tree.build_from_array([1, 3, 5])
		start = time.perf_counter()
		tree.merge(other_tree)
		end = time.perf_counter()
		x7 = x7 + (end - start)

		start = time.perf_counter()
		split_tree = tree.split(a[i])
		end = time.perf_counter()
		x8 = x8 + (end - start)

	#file = open("CartesialTree_1000.txt", "w")
	file = open("CartesialTree_10000.txt", "w")
	#file = open("CartesialTree_100000.txt", "w")
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
	start = time.perf_counter()
	tree.build_from_array(a)
	end = time.perf_counter()
	file = open("CartesialTree_1000.txt", "w")
	file.write('Running time of the algorithm for creating a tree for a given array:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.inorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the centered tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.preorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the direct tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.postorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the reverse tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.find(34)
	end = time.perf_counter()
	#if tree.find(202):
	#	print("Value is in tree")
	#else:
	#	print("Value is not in tree")
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the algorithm for searching for an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.insert(1)
	end = time.perf_counter()
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the algorithm for insert an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.delete(1)
	end = time.perf_counter()
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the algorithm for deleting an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	other_tree = CartesianSearchTree('numeric')
	other_tree.build_from_array([1, 3, 5])
	tree.merge(other_tree)
	start = time.perf_counter()
	tree.merge(other_tree)
	end = time.perf_counter()
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the algorithm for merging 2 trees:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	split_tree = tree.split(34)
	end = time.perf_counter()
	file = open("CartesialTree_1000.txt", "a")
	file.write('Running time of the algorithm for split operation in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	tree = CartesianSearchTree('numeric')
	random.seed(2)
	a = random.sample(range(100000), 10000)
	print(len(a), '\n', a)

	start = time.perf_counter()
	tree.build_from_array(a)
	end = time.perf_counter()
	file = open("CartesialTree_10000.txt", "w")
	file.write('Running time of the algorithm for creating a tree for a given array:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.inorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the centered tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.preorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the direct tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.postorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the reverse tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.find(34)
	end = time.perf_counter()
	#if tree.find(202):
	#	print("Value is in tree")
	#else:
	#	print("Value is not in tree")
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the algorithm for searching for an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.insert(1)
	end = time.perf_counter()
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the algorithm for insert an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.delete(1)
	end = time.perf_counter()
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the algorithm for deleting an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	other_tree = CartesianSearchTree('numeric')
	other_tree.build_from_array([1, 3, 5])
	tree.merge(other_tree)
	start = time.perf_counter()
	tree.merge(other_tree)
	end = time.perf_counter()
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the algorithm for merging 2 trees:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	split_tree = tree.split(34)
	end = time.perf_counter()
	file = open("CartesialTree_10000.txt", "a")
	file.write('Running time of the algorithm for split operation in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	tree = CartesianSearchTree('numeric')
	random.seed(3)
	a = random.sample(range(1000000), 100000)
	print(len(a), '\n', a)

	start = time.perf_counter()
	tree.build_from_array(a)
	end = time.perf_counter()
	file = open("CartesialTree_100000.txt", "w")
	file.write('Running time of the algorithm for creating a tree for a given array:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.inorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the centered tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.preorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the direct tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.postorder_traversal(tree.root)
	end = time.perf_counter()
	print('\n')
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the reverse tree traversal algorithm:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.find(34)
	end = time.perf_counter()
	#if tree.find(202):
	#	print("Value is in tree")
	#else:
	#	print("Value is not in tree")
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the algorithm for searching for an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.insert(1)
	end = time.perf_counter()
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the algorithm for insert an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	tree.delete(1)
	end = time.perf_counter()
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the algorithm for deleting an element in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	other_tree = CartesianSearchTree('numeric')
	other_tree.build_from_array([1, 3, 5])
	tree.merge(other_tree)
	start = time.perf_counter()
	tree.merge(other_tree)
	end = time.perf_counter()
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the algorithm for merging 2 trees:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()

	start = time.perf_counter()
	split_tree = tree.split(34)
	end = time.perf_counter()
	file = open("CartesialTree_100000.txt", "a")
	file.write('Running time of the algorithm for split operation in the tree:' + '\n')
	file.write(str(end - start) + '\n')
	file.close()
'''