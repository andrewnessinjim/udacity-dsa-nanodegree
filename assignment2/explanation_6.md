# Intersection and Union with Linked Lists
This document explains the requirements for the problem and design decisions behind the solution in `problem_6.py` file. This problem focuses on learning linked list and does not look at the optimal union and intersection operations. These operations are inbuilt into python.

## Requirements
1. `union(llist_1, llist_2)` function should return the union of two linked lists provided.
2. `intersection(llist_1, llist_2)` function should return the intersection of two linked lists provided.

## Linked List Design
This section describes the reason for including a particular method in the `LinkedListSet` class and also its time complexity.

### Set capability
The linked list class is called `LinkedListSet` because it doesn't allow duplicate elements, which is like a set. This is achieved by maintaining an internal set in `LinkedListSet` class. Then, every time an element is appended to the linked list, we check if the appended value is already present in the internal set. If it is, we discard the append operation. This ensures all the values in the linked list are always unique.

### Appending
Iterating to the end of the list for appending the value would result in `O(n)` operation. Hence, the linked list appends at the `head` pointer itself to enable appending in `O(1)` time. Appending also looks up an internal set as described in previous section. Since looking up a set is `O(1)`, the overall complexity for appending is still `O(1)`.

### Iterable
`LinkedListSet` class also implements the `__iter__` and `__next__` methods to support pythonic iteration. This is not strictly required, but added to keep the code clean. This will ensure custom linked list objects can be iterated like any other native python objects such as list, set etc.

### \_\_contains\_\_
`LinkedListSet` class also implements the `__contains__` method to support the python `in` operator. This is also not strictly required, but added to keep the code clean. Lookup happens in `O(1)` as described in "Appending" section above.

### to_list()
`to_list()` method is added only to make testing easier. Comparing lists is easier than comparing native objects. This method is not used in the union and intersection implementations.

## Time Complexity
The below sections explain the time complexity for creating a list, performing union on 2 lists and intersection on 2 lists.

### Creating the list
The time complexity for creating a `LinkedListSet` object of size `n` is `O(n)`. This is because we have to call append for each element.

Each append operation looks up the internal set, creates a new node, and attaches it to the head, which is `O(1)`. This is because each of these steps need constant time. So overall, creating a `LinkedListSet` is `O(n)`.

### Union
When we perform the union operation on two lists, we iterate over each list one after the other and append the values to a third list. If first list has `m` elements and second list has `n` elements, then we are iterating `m+n` elements in total. For each iteration, we are appending to a third list. The append operation on the list is `O(1)` operation as explained in creating the list section. Hence, the overall complexity is `O((m + n) * 1)`, or `O(m + n)`.

### Intersection
When we perform the intersection operation on two lists, we iterate over the first list, and lookup the second list if the value of the current iteration is present. If it is present, we append this value to a third list. If the first list contains `m` elements, then we iterate `m` times. In each iteration, we look up the second list. This is constant time because `LinkedListSet` maintains an internal set and looking up a set is a constant time operation. If the lookup returns true, then we append the element to the third list. Appending to a list is `O(1)` as explained in creating the list section. In the worst case, all the elements in the first list would be present in the second list. So overall, this would be `O(m * 1 * 1)`, or `O(m)`.

## Space Complexity
Each element of a set is stored in the internal set, and as a node. So this `2n` space. The intersection and union operations use a third list to store the output, before returning it at the end. So the program in its entirety needs `3n` space in the worst case. By dropping the constants, the space complexity is `O(n)`.

## References
[Stackoverflow: Convert list of ints to a joined string](https://stackoverflow.com/questions/3590165/join-a-list-of-items-with-different-types-as-string-in-python)  
[Python Docs: Iterators in Python](https://docs.python.org/3/tutorial/classes.html#iterators)  
[Udacity Knowledge: Maintaining set property](https://knowledge.udacity.com/questions/415843)