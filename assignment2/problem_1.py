class DNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"DNode({self.data})"

class DoublyLinkedList:
    """
    This DoublyLinkedList is not based on any general usage. It is designed to specifically support our LRU cache. Mainly, this class exposes 2 methods - append_to_tail and move_node_to_tail. These are used by the cache to ensure that the LRU element is always at the head, and MRU element is always at the tail
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def append_to_tail(self, data):
        """
        This method returns a reference to the created node after appending. This works in constant time as there is no traversing involved. The cache also stores the returned reference along with the key and value.
        """
        dnode = DNode(data)
        if self.head is None:
            self.head = dnode
            self.tail = dnode
            return dnode
        
        dnode.prev = self.tail
        self.tail.next = dnode
        self.tail = dnode
        return dnode

    def peek_head(self):
        """
        The cache uses this method to get the LRU key in constant time.
        """
        if self.head:
            return self.head.data

    def pop_head(self):
        """
        The cache uses this method to drop the LRU key in constant time. This method could have returned the popped key as well, but having a separate method such as peek_head() to look at the value improves code readability.
        """
        if self.head:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None

            # If the last element is popped
            if self.head is None:
                self.tail = None

    def move_node_to_tail(self, new_tail: DNode):
        """
        This works in constant time because the node to be moved is already provided by the cache, there is no need to traverse. Node can be moved to tail by altering a fixed number of links.
        """
        if new_tail is self.tail: #Key is already MRU
            return
        
        if new_tail is self.head: #Edge case: head key should be tail now
            self.head = self.head.next
            self.head.prev = None

        else:
            """
            Link up the nodes on either side of the new_tail.
            For example, if the list is 1 -- 2 -- 3 and 2 is the new tail, this else block links up 1 and 3 in both directions, so the list becomes 1 -- 3 now.
            """ 
            prev_node = new_tail.prev
            next_node = new_tail.next
            prev_node.next = next_node
            next_node.prev = prev_node

        # Move the new_tail to the tail of the list
        self.tail.next = new_tail
        new_tail.prev = self.tail
        self.tail = new_tail
        new_tail.next = None

    def forward_list(self): # For debugging purpose only
        forward = list()
        cur = self.head
        while cur:
            forward.append(cur.data)
            cur = cur.next
        return forward

    def reverse_list(self): # For debugging purpose only
        reverse = list()
        cur = self.tail
        while cur:
            reverse.append(cur.data)
            cur = cur.prev

        return reverse

# Helper function for testing
def test(expected, actual):
    message =f"Expected: {expected}. Actual: {actual}"
    if expected == actual:
        print (f"Pass: {message}")
    else:
        print (f"Fail: {message}")

# This method tests only the functionalities of the doubly linked list independent of the cache. This follows the step-by-step development and testing approach, which increases the chance of quicker success.
def test_doubly_linked_list():
    dlist = DoublyLinkedList()

    # Create a list with 3 values
    dlist.append_to_tail(1)
    new_tail = dlist.append_to_tail(2)
    dlist.append_to_tail(3)

    # Test if forward and reverse links are correct
    test([1, 2, 3], dlist.forward_list())
    test([3, 2, 1], dlist.reverse_list())

    # Move 2 to the end of the list
    dlist.move_node_to_tail(new_tail)

    # Test if Node(2) was moved successfully to the tail
    test([1,3,2], dlist.forward_list())
    test([2,3,1], dlist.reverse_list())

    # Remove the head node
    dlist.pop_head()

    # Test if 1 was removed from list
    test([3,2], dlist.forward_list())
    test([2,3], dlist.reverse_list())

    # Pop all remaining elements
    dlist.pop_head()
    dlist.pop_head()

    # Test if list is empty now
    test([], dlist.forward_list())
    test([], dlist.reverse_list())

    # Add elements again
    dlist.append_to_tail(1)
    dlist.append_to_tail(2)
    dlist.append_to_tail(3)

    test([1, 2, 3], dlist.forward_list())
    test([3, 2, 1], dlist.reverse_list())

# Uncomment below function call to test DoublyLinkedList independently.
# test_doubly_linked_list()

class LRU_Cache(object):
    def __init__(self, capacity):
        self._MAX_SIZE = capacity
        self.cache = dict()
        self.current_size = 0
        self.lru_tracker = DoublyLinkedList()
        pass

    def get(self, key):
        if key not in self.cache: # Scenario 1 from explanation
            return -1
        
        # Scenario 2 from explanation
        self._mark_key_as_mru(key)
        return self.cache[key][0]

    def set(self, key, value):
        # Scenario 3 from explanation
        if key in self.cache:
            _, dnode = self.cache[key]
            self.cache[key] = (value, dnode)
            self._mark_key_as_mru(key)
            return

        # Scenario 4 from explanation
        if self.current_size == self._MAX_SIZE:
            lru_key = self._get_lru_key()
            del self.cache[lru_key]
            self._drop_lru_key()
            self.current_size -= 1

        # Below is common for both scenario 4 and 5 from explanation
        dnode = self.lru_tracker.append_to_tail(key)
        self.cache[key] = (value, dnode)
        self.current_size += 1
        return

    """
    _drop_lru_key and _mark_key_as_mru are used to ensure the LRU key is always at the head and MRU key at the tail. _get_lru_key returns the head value of the doubly linked list. Because of the way the list is maintained, this is always the LRU key. All these 3 operations work on constant time as explained in the DoublyLinkedList class' comments.
    """
    def _drop_lru_key(self):
        self.lru_tracker.pop_head()

    def _get_lru_key(self):
        return self.lru_tracker.peek_head()

    def _mark_key_as_mru(self, key):
        dnode = self.cache[key][1]
        self.lru_tracker.move_node_to_tail(dnode)

    def __repr__(self):
        s = "--------------------\n"
        s += "CACHE:\n"
        s += str(self.cache) + "\n"
        s += "LRU_TRACKER: \n"
        s += f"LRU end -> {self.lru_tracker.forward_list()} <- MRU end\n"

        return s


def test_case_1():
    # Get values without setting anything. We should always get -1
    our_cache = LRU_Cache(5)

    print("---------Test case 1---------")
    test(our_cache.get(1), -1)
    test(our_cache.get(4), -1)
    test(our_cache.get(5), -1)

def test_case_2():
    # Set one value. Get that value, then get non-existent values.
    our_cache = LRU_Cache(5)
    our_cache.set(1, 10)

    print("---------Test case 2---------")
    # Expect 10 to be returned as it is set above
    test(our_cache.get(1), 10)

    #Expect -1 to be returned because 2 was never set
    test(our_cache.get(2), -1)

def test_case_3():
    # Set 10 different keys. The first five keys should return -1 as they will be dropped, second five keys should return correct values
    our_cache = LRU_Cache(5)
    our_cache.set(1, 10)    
    our_cache.set(2, 20)
    our_cache.set(3, 30)
    our_cache.set(4, 40)
    our_cache.set(5, 50)
    our_cache.set(6, 60)
    our_cache.set(7, 70)
    our_cache.set(8, 80)
    our_cache.set(9, 90)
    our_cache.set(10, 100)

    print("---------Test case 3---------")
    test(our_cache.get(1), -1)    
    test(our_cache.get(2), -1)
    test(our_cache.get(3), -1)
    test(our_cache.get(4), -1)
    test(our_cache.get(5), -1)
    test(our_cache.get(6), 60)
    test(our_cache.get(7), 70)
    test(our_cache.get(8), 80)
    test(our_cache.get(9), 90)
    test(our_cache.get(10), 100)

def test_case_4():
    #Set 6 keys. The first key should now return -1 because it was the LRU element when 6th element was inserted. So it should be dropped
    our_cache = LRU_Cache(5)
    our_cache.set(1, 10)    
    our_cache.set(2, 20)
    our_cache.set(3, 30)
    our_cache.set(4, 40)
    our_cache.set(5, 50)
    our_cache.set(6, 60)

    print("---------Test case 4---------")
    test(our_cache.get(1), -1)    
    test(our_cache.get(2), 20)
    test(our_cache.get(3), 30)
    test(our_cache.get(4), 40)
    test(our_cache.get(5), 50)
    test(our_cache.get(6), 60)

def test_case_5():
    # Set 5 keys. Reset 1st key. First key now becomes MRU element. Then set 6th key. The first key should still be in the cache. The second key should be dropped.
    our_cache = LRU_Cache(5)
    our_cache.set(1, 10)    
    our_cache.set(2, 20)
    our_cache.set(3, 30)
    our_cache.set(4, 40)
    our_cache.set(5, 50)

    # Reset 1st key. This makes it MRU element.
    our_cache.set(1, 100)

    # Adding another key should now drop key 2 and not key 1 because key 1 was just accessed
    our_cache.set(6, 60)

    print("---------Test case 4---------")
    test(our_cache.get(1), 100)
    test(our_cache.get(2), -1)

def test_case_5():
    # This is similar to test case 4. But instead of resetting the 1st key, it gets the first key. This should also make it the MRU element. So same behavior is expected.
    our_cache = LRU_Cache(5)
    our_cache.set(1, 10)    
    our_cache.set(2, 20)
    our_cache.set(3, 30)
    our_cache.set(4, 40)
    our_cache.set(5, 50)

    # Read 1st key. This makes it MRU element.
    our_cache.get(1)

    # Adding another key should now drop key 2 and not key 1 because key 1 was just accessed
    our_cache.set(6, 60)

    print("---------Test case 5---------")
    test(our_cache.get(1), 10)
    test(our_cache.get(2), -1)


test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()