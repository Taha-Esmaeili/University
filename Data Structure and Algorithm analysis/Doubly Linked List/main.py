class Linkedlist:
    """
    A class representing a doubly linked list with basic operations for inserting,
    deleting, and accessing elements. The list has a header and trailer node as sentinels.
    """


    class _Node:
        """
        A lightweight, non-public class for storing a doubly linked node.
        """

        def __init__(self, element, prev, next):
            """
            Initialize a node with an element and links to the previous and next nodes.

            Parameters:
            element: The data to be stored in the node.
            prev (_Node): The previous node in the list.
            next (_Node): The next node in the list.
            """
            self._element = element
            self._prev = prev
            self._next = next

    
    def __init__ (self):
        """
        Initialize an empty linked list with header and trailer sentinels.
        """
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    
    def __len__ (self):
       """
        Return the number of elements in the linked list.

        Returns:
        int: The number of elements in the list.
        """
         return self._size
    

    def is_empty(self):
        """
        Check if the linked list is empty.

        Returns:
        bool: True if the list is empty, False otherwise.
        """
        return self._size == 0
    

    def _insert_between(self, element, predecessor, successor):
        """
        Insert an element between two existing nodes and return the new node.

        Parameters:
        element: The data to be stored in the new node.
        predecessor (_Node): The node before the position of the new node.
        successor (_Node): The node after the position of the new node.

        Returns:
        _Node: The newly created node.
        """
        newest = self._Node(element, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest
    

    def _delete_node(self, node):
        """
        Delete a node from the linked list and return its element.

        Parameters:
        node (_Node): The node to be deleted.

        Returns:
        element: The data stored in the deleted node.
        """
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element
    
    def access_default(self, value): # Without changing the list
        """
        Access an element in the list without modifying the list.

        Parameters:
        value: The value to be accessed.

        Returns:
        int: The position (cost) of the element in the list, or None if not found.
        """
        current = self._header
        for cost in range(self._size):
            current = current._next
            if value == current._element:
                return cost



    def access_insertion(self, value): # With changing the list
        """
        Access an element in the list and move it to the front if found.

        Parameters:
        value: The value to be accessed and potentially moved.

        Returns:
        tuple: (cost, operation) where 'cost' is the position of the element
               and 'operation' is 1 if the element was moved, 0 otherwise.
        """
        current = self._header
        for cost in range(self._size):
            current = current._next
            if value == current._element:
                if cost == 0:
                    return (cost, 0)

                # Move the accessed element to the front of the list
                self._insert_between(value, self._header, self._header._next)
                self._delete_node(current)
                return (cost, 1)


import random

def list_generator(n):
    """
    Generate two linked lists with random elements.

    Parameters:
    n (int): The number of elements in each linked list.

    Returns:
    tuple: A tuple containing two Linkedlist instances.
    """
    Default_list = Linkedlist()
    Insertion_list = Linkedlist()
    for element in random.sample(range(1, n+1), n):
        Default_list._insert_between(element, Default_list._trailer._prev, Default_list._trailer)
        Insertion_list._insert_between(element,Insertion_list._trailer._prev, Insertion_list._trailer)

    return Default_list, Insertion_list



def Normal_cost(list, sequence):
    """
    Calculate the total access cost for a sequence of elements using the default access method.

    Parameters:
    list (Linkedlist): The linked list to access.
    sequence (list): The sequence of elements to access.

    Returns:
    str: The total cost as a string.
    """
    total_cost = 0
    for element in sequence:
        total_cost += list.access_default(element)
    return str(total_cost)



def Insertion_cost(list, sequence):
    """
    Calculate the total access cost for a sequence of elements using the insertion access method.

    Parameters:
    list (Linkedlist): The linked list to access.
    sequence (list): The sequence of elements to access.

    Returns:
    str: The total cost as a string with the format 'cost + count*c', where 'c' is the number
         of times an element was moved to the front.
    """
    total_cost = 0
    c = 0
    for element in sequence:
        acces_insertion = list.access_insertion(element)
        total_cost += acces_insertion[0]
        c += acces_insertion[1]
        
    return f'{total_cost} + {c}c'



# ==============================================
# 1

if __name__ == '__main__':
    n = 10000

    # Generate linked lists with 10,000 elements
    Default_list, Insertion_list = list_generator(10000)

    # Create a sequence of elements from 1 to 10,000
    sequence = [ i for i in range(1,10001)]

    # Calculate and print the total access cost for each linked list
    print('Normal Linked list:', Normal_cost(Default_list, sequence))
    print('Insertion Linked list:', Insertion_cost(Insertion_list, sequence))


# ===============================================
# 2
if __name__ == '__main__':
    n = 10000

    # Generate linked lists with 10,000 elements
    default_list, insertion_list = list_generator(n)

    # Create a repeated sequence of the first 10 elements
    sequence = [i for i in range(1, 11) for _ in range(1000)]

    # Calculate and print the total access cost for each linked list
    print('Normal linked list: ', Normal_cost(default_list, sequence))
    print('Insertion linked list: ', Insertion_cost(insertion_list, sequence))

# ====================================================
import numpy as np

if __name__ == '__main__':
    n = 10000

    # Generate linked lists with 10,000 elements
    default_list, insertion_list = list_generator(n)

    # Generate a random sequence of elements with a normal distribution
    np.random.seed(0)
    a = np.random.normal(5000, 1000, size=10000)
    a = a.round(decimals=0, out=None)
    a = abs(a)
    sequence = a[a < 10000 ]

    # Calculate and print the total access cost for each linked list
    print('Normal linked list: ', Normal_cost(default_list, sequence))
    print('Insertion linked list: ', Insertion_cost(insertion_list, sequence))
