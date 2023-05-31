import time

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
		if self.root is None:
			self.root = Node(value)
			return

		if self.data_type == 'numeric':
			node = Node(value)
			curr = self.root

			while curr.right is not None and curr.right.value > node.value:
				curr = curr.right

			if curr.right is None:
				node.parent = curr
				curr.right = node
			else:
				node.left = curr.right
				node.left.parent = node
				node.parent = curr
				curr.right = node

		else:
			words = value.split(' ')
			node = Node(words[0])
			curr = self.root

			while curr.right is not None and curr.right.value.split(' ')[0] > words[0]:
				curr = curr.right

			if curr.right is None:
				node.parent = curr
				curr.right = node
			else:
				node.left = curr.right
				node.left.parent = node
				node.parent = curr
				curr.right = node

	def search(self, value):
		if self.root is None:
			return False

		if self.data_type == 'numeric':
			curr = self.root

			while curr is not None and curr.value != value:
				if value < curr.value:
					curr = curr.left
				else:
					curr = curr.right

			if curr is not None:
				return True
			else:
				return False

		else:
			words = value.split(' ')
			curr = self.root

			while curr is not None and curr.value.split(' ')[0] != words[0]:
				if words[0] < curr.value.split(' ')[0]:
					curr = curr.left
				else:
					curr = curr.right

			if curr is not None:
				return True
			else:
				return False

	def delete(self, value):
		if self.root is None:
			return

		if self.data_type == 'numeric':
			curr = self.root

			while curr is not None and curr.value != value:
				if value < curr.value:
					curr = curr.left
				else:
					curr = curr.right

			if curr is None:
				return

			if curr.left is None and curr.right is None:
				if curr.parent is None:
					self.root = None
				elif curr.parent.left == curr:
					curr.parent.left = None
				else:
					curr.parent.right = None

			elif curr.left is None or curr.right is None:
				if curr.parent is None:
					if curr.left is not None:
						self.root = curr.left
					else:
						self.root = curr.right
				elif curr.parent.left == curr:
					if curr.left is not None:
						curr.parent.left = curr.left
						curr.left.parent = curr.parent
					else:
						curr.parent.left = curr.right
						curr.right.parent = curr.parent
				else:
					if curr.left is not None:
						curr.parent.right = curr.left
						curr.left.parent = curr.parent
					else:
						curr.parent.right = curr.right
						curr.right.parent = curr.parent

			else:
				successor = curr.right

				while successor.left is not None:
					successor = successor.left

				curr.value = successor.value

				if successor.parent.left == successor:
					successor.parent.left = successor.right
				else:
					successor.parent.right = successor.right

				if successor.right is not None:
					successor.right.parent = successor.parent

		else:
			words = value.split(' ')
			curr = self.root

			while curr is not None and curr.value.split(' ')[0] != words[0]:
				if words[0] < curr.value.split(' ')[0]:
					curr = curr.left
				else:
					curr = curr.right

				if curr is None:
					return

				if curr.left is None and curr.right is None:
					if curr.parent is None:
						self.root = None
					elif curr.parent.left == curr:
						curr.parent.left = None
					else:
						curr.parent.right = None

				elif curr.left is None or curr.right is None:
					if curr.parent is None:
						if curr.left is not None:
							self.root = curr.left
						else:
							self.root = curr.right
					elif curr.parent.left == curr:
						if curr.left is not None:
							curr.parent.left = curr.left
							curr.left.parent = curr.parent
						else:
							curr.parent.left = curr.right
							curr.right.parent = curr.parent
					else:
						if curr.left is not None:
							curr.parent.right = curr.left
							curr.left.parent = curr.parent
						else:
							curr.parent.right = curr.right
							curr.right.parent = curr.parent

				else:
					successor = curr.right

					while successor.left is not None:
						successor = successor.left

					curr.value = successor.value

					if successor.parent.left == successor:
						successor.parent.left = successor.right
					else:
						successor.parent.right = successor.right

					if successor.right is not None:
						successor.right.parent = successor.parent

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
	start = time.perf_counter()
	tree.insert(5)
	end = time.perf_counter()
	print("Время работы алгоритма: ", end - start)
