class Node:
    """A node in a doubly linked list."""
    __slots__ = ("value", "prev", "next")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """A simple doubly linked list implementation."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def append(self, value):
        """Add a node with the given value to the end of the list."""
        new_node = Node(value)
        if self.tail is None:  # empty list
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        return new_node

    def prepend(self, value):
        """Add a node with the given value to the beginning of the list."""
        new_node = Node(value)
        if self.head is None:  # empty list
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
        return new_node

    def insert_after(self, node, value):
        """Insert a new node with `value` after `node`."""
        if node is None:
            raise ValueError("The given node cannot be None")
        new_node = Node(value)
        new_node.prev = node
        new_node.next = node.next
        if node.next:
            node.next.prev = new_node
        else:
            self.tail = new_node
        node.next = new_node
        self._size += 1
        return new_node

    def insert_before(self, node, value):
        """Insert a new node with `value` before `node`."""
        if node is None:
            raise ValueError("The given node cannot be None")
        new_node = Node(value)
        new_node.next = node
        new_node.prev = node.prev
        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node
        node.prev = new_node
        self._size += 1
        return new_node

    def remove(self, node):
        """Remove `node` from the list."""
        if node is None:
            raise ValueError("The node to remove cannot be None")
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1
        return node.value

    def pop_front(self):
        """Remove and return the first element."""
        if self.head is None:
            raise IndexError("pop from empty list")
        return self.remove(self.head)

    def pop_back(self):
        """Remove and return the last element."""
        if self.tail is None:
            raise IndexError("pop from empty list")
        return self.remove(self.tail)

    def find(self, value):
        """Return the first node containing `value`, or None if not found."""
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def __iter__(self):
        """Iterate forward over the values."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self):
        """Iterate backward over the values."""
        current = self.tail
        while current:
            yield current.value
            current = current.prev

    def clear(self):
        """Remove all elements from the list."""
        current = self.head
        while current:
            nxt = current.next
            current.prev = current.next = None
            current = nxt
        self.head = self.tail = None
        self._size = 0

    def to_list(self):
        """Return a Python list containing all elements in order."""
        return list(iter(self))

    def __repr__(self):
        values = ", ".join(repr(v) for v in self)
        return f"DoublyLinkedList([{values}])"