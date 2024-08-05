class Node:
    """
    A class representing a node in a binary search tree.

    Attributes:
    element: The value stored in the node.
    left (Node): The left child node.
    right (Node): The right child node.
    parent (Node): The parent node.
    """
    def __init__(self, val):
        """
        Initialize a new node with a given value.

        Parameters:
        val: The value to be stored in the node.
        """
        self.left = None
        self.right = None
        self.parent = None
        self.element = val

    def isleaf(self):
        """
        Check if the node is a leaf node (has no children).

        Returns:
        bool: True if the node is a leaf, False otherwise.
        """
        return self.right is None and self.left is None

    def display(self):
        """
        Print a visual representation of the tree rooted at the current node.

        This function prints the tree in a horizontal format, with the root at the top.
        """
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """
        Return a list of strings representing the tree, along with its width,
        height, and the horizontal coordinate of the root.

        This is a helper function used by the display method.

        Returns:
        list: A list of strings representing the tree.
        int: The width of the tree.
        int: The height of the tree.
        int: The horizontal coordinate of the root.
        """
        # No child
        if self.right is None and self.left is None:
            line = '%s' % self.element
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.element
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.element
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.element
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


########################################
class BST:
    """
    A class representing a Binary Search Tree (BST).

    Attributes:
    root (Node): The root node of the tree.
    """
    def __init__(self):
        """
        Initialize an empty Binary Search Tree.
        """
        self.root = None

    def get_root(self):  
        """
        Get the root node of the tree.

        Returns:
        Node: The root node of the tree.
        """
        return self.root

    def set_root(self, node):
        """
        Set the root node of the tree.

        Parameters:
        node (Node): The node to set as the root.

        Returns:
        Node: The node that was set as the root, or a message indicating the tree already has a root.
        """
        if self.root is None:
            self.root = node
            return node
        return 'Tree already has a root'

    def find_element(self, element):  
        """
        Find a node with the given element in the tree.

        Parameters:
        element: The value to search for.

        Returns:
        Node: The node with the given element, or None if not found.
        """
        def _find_element(r, element):
            while r is not None:
                if r.element == element:
                    return r
                elif r.element < element:
                    r = r.right
                else:
                    r = r.left
            return None

        return _find_element(self.root, element)

    def find_min(self):  
        """
        Find the node with the minimum value in the tree.

        Returns:
        Node: The node with the minimum value.
        """
        def _find_min(r):
            while r.left is not None:
                r = r.left
            return r

        return _find_min(self.root)

    def successor(self, node):
        """
        Find the in-order successor of a given node.

        Parameters:
        node (Node): The node whose successor is to be found.

        Returns:
        Node: The in-order successor of the given node, or None if no successor exists.
        """
        if node.right is not None:
            temp = node.right
            while temp.left is not None:
                temp = temp.left
            return temp

        else:
            if node.parent is not None:
                temp = node.parent
                while temp.parent is not None and temp != temp.parent.left:
                    temp = temp.parent

                if temp.parent is None:
                    return None
                return temp.parent

        return None

    def delete_min(self):
        """
        Delete the node with the minimum value in the tree.
        """
        min_node = self.find_min()
        self.delete_element(min_node.element)

    def delete_element(self, element):
        """
        Delete a node with the given element from the tree.

        Parameters:
        element: The value of the node to be deleted.

        Returns:
        Node: The node that was deleted, or None if the node was not found.
        """
        node = BST.find_element(self, element)
        if node is None:
            return None

        elif node.left is None and node.right is not None:
            node.right.parent = node.parent
            if node.parent is None:
                self.root = node.right
            elif node.parent.right == node:
                node.parent.right = node.right
            elif node.parent.left == node:
                node.parent.left = node.right

        elif node.right is None and node.left is not None:
            node.left.parent = node.parent
            if node.parent is None:
                self.root = node.left
            elif node.parent.right == node:
                node.parent.right = node.left
            elif node.parent.left == node:
                node.parent.left = node.left

        elif node.left is None and node.right is None:
            if node.parent is None:
                self.root = None
            elif node.parent.right == node:
                node.parent.right = None
            else:
                node.parent.left = None


        else:
            successor = self.successor(node)
            temp = successor.element
            self.delete_element(successor.element)
            node.element = temp

        return node

    def insert_element(self, element):
        """
        Insert a new element into the tree.

        Parameters:
        element: The value of the new element to be inserted.

        Returns:
        Node: The newly inserted node, or the node if it already exists.
        """

        if self.root is None:
            node = Node(element)
            self.set_root(node)
            return node

        def _insert(r, node):  # Here r stands for the root of the subtree and n stands for the new element
            """
            Helper function to recursively insert a node into the tree.

            Parameters:
            r (Node): The root of the subtree.
            node (Node): The new node to be inserted.

            Returns:
            Node: The inserted node.
            """
            if r.element > node.element:
                if r.left is None:
                    r.left = node
                    node.parent = r
                    return node
                return _insert(r.left, node)

            elif r.element < node.element:
                if r.right is None:
                    r.right = node
                    node.parent = r
                    return node
                return _insert(r.right, node)

        node = self.find_element(element)
        if node:
            return node
        else:
            node = Node(element)
            return _insert(self.root, node)


class SplayTree(BST):
    """
    A class representing a Splay Tree, a self-adjusting binary search tree.

    This class extends the basic BST class with splaying operations that move
    accessed elements closer to the root to optimize future access operations.
    """
    def __init__(self):
        """
        Initialize an empty Splay Tree by calling the superclass constructor.
        """
        super().__init__()

    def splay(self, node):
        """
        Splay the tree with the given node by moving it to the root using rotations.

        Parameters:
        node (Node): The node to splay.
        """
        if node.parent:
            while node.parent is not None:
                if node.parent.parent is None:  # Zig step
                    if node == node.parent.left:
                        self._rotate_right(node.parent)
                    else:
                        self._rotate_left(node.parent)

                elif node == node.parent.left and node.parent == node.parent.parent.left:  # Zig-Zig step
                    self._rotate_right(node.parent.parent)
                    self._rotate_right(node.parent)
                elif node == node.parent.right and node.parent == node.parent.parent.right:  # Zig-Zig step
                    self._rotate_left(node.parent.parent)
                    self._rotate_left(node.parent)
                elif node == node.parent.right and node.parent == node.parent.parent.left:  # Zig-Zag step
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)
                elif node == node.parent.left and node.parent == node.parent.parent.right:  # Zig-Zag step
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)

    def insert(self, element):
        """
        Insert a new element into the Splay Tree and splay the tree with the new node.

        Parameters:
        element: The value of the new element to be inserted.

        Returns:
        Node: The newly inserted node.
        """
        node = super().insert_element(element)
        if node:
            self.splay(node)
        return node

    def search(self, element):
        """
        Search for an element in the Splay Tree and splay the tree with the found node.

        Parameters:
        element: The value to search for.

        Returns:
        Node: The node with the given element, or None if not found.
        """
        node = super().find_element(element)
        if node:
            self.splay(node)
        return node

    def delete(self, element):
        """
        Delete a node with the given element from the Splay Tree and splay the tree
        with the parent of the deleted node.

        Parameters:
        element: The value of the node to be deleted.

        Returns:
        Node: The node that was deleted, or None if the node was not found.
        """
        node = super().delete_element(element)
        if node is not None and node.parent is not None:
            self.splay(node.parent)
        return node

    def _rotate_right(self, node):
        """
        Perform a right rotation around the given node.

        Parameters:
        node (Node): The node around which to perform the right rotation.
        """
        child = node.left
        parent = node.parent
        if child.right is not None:
            child.right.parent = node
        if parent is None:
            self.root = child
        if parent:
            if node == parent.left:
                parent.left = child
            else:
                parent.right = child

        child.parent = parent
        node.left = child.right
        child.right = node
        node.parent = child

    def _rotate_left(self, node):
        """
        Perform a left rotation around the given node.

        Parameters:
        node (Node): The node around which to perform the left rotation.
        """
        child = node.right
        parent = node.parent
        if child.left is not None:
            child.left.parent = node
        if parent is None:
            self.root = child
        if parent:
            if node == parent.left:
                parent.left = child
            else:
                parent.right = child

        child.parent = parent
        node.right = child.left
        child.left = node
        node.parent = child



# Sequence (part 1)
def main_1():
    """
    Execute a sequence of insertions and deletions on a BST and a Splay Tree.
    The sequence is read from a file called 'sequence.txt', where each line contains
    operations (insertion or deletion) to be performed on the trees.

    The state of the trees is displayed after each sequence of operations.
    """
    bst = BST()
    splay_tree = SplayTree()

    with open('sequence.txt', 'r') as f:
        sequences = [line.split() for line in f.readlines() if line.strip()]

    for i, sequence in enumerate(sequences):
        print(f'---Sequence {i + 1}---')

        for block in sequence:
            operator = block[-1]

            if operator == '+':
                element = int(block[:-1])
                bst.insert_element(element)
                splay_tree.insert(element)

            if operator == '-':
                element = int(block[:-1])
                bst.delete_element(element)
                splay_tree.delete(element)

        bst.get_root().display()
        splay_tree.get_root().display()

# main_1()



# access lists (part2)
class BSTCounter(BST):
    """
    A class representing a Binary Search Tree (BST) with an added feature to track
    the cost of accessing elements.

    This class extends the basic BST class by adding a method to find elements while
    counting the number of comparisons made during the search.
    """
    def find_with_cost(self, element: int) -> tuple:
        """
        Find a node with the given element in the tree and return the node along with
        the cost (number of comparisons) of finding the element.

        Parameters:
        element (int): The value to search for.

        Returns:
        tuple: A tuple containing the node with the given element and the cost (int)
               of finding the element. If the element is not found, returns (None, cost).
        """
        def _find_with_cost(root, element, cost=0):
            if root.element == element:
                return root, cost

            elif root.element < element:
                if root.right is not None:
                    return _find_with_cost(root.right, element, cost + 1)

            elif root.element > element:
                if root.left is not None:
                    return _find_with_cost(root.left, element, cost + 1)

        return _find_with_cost(self.root, element)

class SplayTreeCounter(BSTCounter, SplayTree):
    """
    A class representing a Splay Tree with an added feature to track the cost of accessing
    elements and splaying the tree.

    This class extends both BSTCounter and SplayTree classes, combining the features of
    splaying and access cost tracking.
    """
    def _splay_with_cost(self, node):
        """
        Splay the tree with the given node and track the cost (number of rotations) of splaying.

        Parameters:
        node (Node): The node to splay.

        Returns:
        int: The cost (number of rotations) of splaying the node.
        """
        cost = 0
        if node.parent:
            while node.parent is not None:
                if node.parent.parent is None:  # Zig step
                    if node == node.parent.left:
                        self._rotate_right(node.parent)
                        cost += 1
                    else:
                        self._rotate_left(node.parent)
                        cost += 1
                elif node == node.parent.left and node.parent == node.parent.parent.left:  # Zig-Zig step
                    self._rotate_right(node.parent.parent)
                    self._rotate_right(node.parent)
                    cost += 2
                elif node == node.parent.right and node.parent == node.parent.parent.right:  # Zig-Zig step
                    self._rotate_left(node.parent.parent)
                    self._rotate_left(node.parent)
                    cost += 2
                elif node == node.parent.right and node.parent == node.parent.parent.left:  # Zig-Zag step
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)
                    cost += 2
                elif node == node.parent.left and node.parent == node.parent.parent.right:  # Zig-Zag step
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                    cost += 2
        return cost

    def find_with_cost(self, element: int) -> tuple:
        """
        Find a node with the given element in the Splay Tree, splay the tree with the node,
        and return the node along with the total cost of finding and splaying the element.

        Parameters:
        element (int): The value to search for.

        Returns:
        tuple: A tuple containing the node with the given element and the total cost (int)
               of finding and splaying the element.
        """
        node, cost = super().find_with_cost(element)
        if node:
            cost += self._splay_with_cost(node)
        return node, cost



from random import shuffle


def access(bst, splay_tree, access_list):
    """
    Access a list of elements in both a BST and a Splay Tree, tracking the cost of each access.

    Parameters:
    bst (BSTCounter): The BST to access.
    splay_tree (SplayTreeCounter): The Splay Tree to access.
    access_list (list): The list of elements to access.

    Returns:
    tuple: A tuple containing the total cost of accessing the elements in the BST and the Splay Tree.
    """
    bst_cost = 0
    splay_tree_cost = 0
    for element in access_list:
        bst_cost += bst.find_with_cost(element)[1]
        splay_tree_cost += splay_tree.find_with_cost(element)[1]

    return bst_cost, splay_tree_cost

def main_2():
    """
    Generate a random sequence of elements, insert them into both a BST and a Splay Tree,
    and then access the elements from predefined access lists to compare the access costs.

    The access lists are read from files 'accesslist1.txt', 'accesslist2.txt', and 'accesslist3.txt'.
    """
    n = 10000
    shuffle(sequence := list(range(1, n + 1)))
    bst = BSTCounter()
    splay_tree = SplayTreeCounter()
    for element in sequence:
        bst.insert_element(element)
        splay_tree.insert(element)

    def access1():
        print('---Access List 1---')
        with open('accesslist1.txt', 'r') as file1:
            access_list1 = list(map(int, file1.read().split()))
        bst_cost, splay_tree_cost = access(bst, splay_tree, access_list1)
        print(f'Bst: {bst_cost}')
        print(f'Splay Tree: {splay_tree_cost}')

    def access2():
        print('---Access List 2---')
        with open('accesslist2.txt', 'r') as file1:
            access_list2 = list(map(int, file1.read().split()))
        bst_cost, splay_tree_cost = access(bst, splay_tree, access_list2)
        print(f'Bst: {bst_cost}')
        print(f'Splay Tree: {splay_tree_cost}')

    def access3():
        print('---Access List 3---')
        with open('accesslist3.txt', 'r') as file1:
            access_list3 = list(map(int, file1.read().split()))
        bst_cost, splay_tree_cost = access(bst, splay_tree, access_list3)
        print(f'Bst: {bst_cost}')
        print(f'Splay Tree: {splay_tree_cost}')

    access1()
    access2()
    access3()


main_2()
