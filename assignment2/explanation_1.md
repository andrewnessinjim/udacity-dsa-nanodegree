# LRU Cache with read and write operations of O(1) complexity

This document explains the requirements for the problem and design decisions behind the solution in `problem_1.py` file.

## Glossary
* **Cache** - Storage that supports storing and reading values very quickly.
* **LRU (Least recently used) element** - The element in the cache that was accessed before any of the other elements is considered to be the LRU element. Both reading and writing a value in the cache is considered to be an access.
* **MRU (Most recently used) element** - The element in the cache that was accessed after any of the other elements is considered to be the MRU element.

## Assumption
   A real-world cache is normally stored in a memory with faster access compared to the memory where the data for the cache originally comes from. We will use a Python class to represent the cache for demonstration purpose. 

## Requirements
1.  Implement a cache that is constrained by a size, `_MAX_SIZE`.
2.  At any point in time, the cache should not hold more than `_MAX_SIZE` number of MRU elements. Both reading and writing elements should be considered as an access.
3.  Both `set` and `get` operations on the cache should have time complexity of `O(1)`

## Design Decisions (with time complexity reasoning)
Since we want the `set` and `get` operations to happen in constant time, we choose a map (dictionary in python) to store the key value pairs. Below statement follows from this because python dictionaries provide constant time read and write given the key:

> Statement 1: Reading and writing from a python dictionary is `O(1)`
 
If the requirement did not state the size should be constrained, no further data structures would have been required. But since the size is constrained, we need to track the LRU (or MRU) elements. Whenever the cache is full and another entry needs to be stored, we drop the LRU element. We use a doubly linked list (abbreviated as dlist) with a head and tail to track the LRU elements. In our implementation, we will store only the keys. dlists allow us to alter the order of its data in constant time. We need this feature to ensure `O(1)` for all operations.

Let's say the cache currently has 5 keys - `1, 2, 3, 4, 5`, accessed in that order. The head of the dlist will point to 1 and the tail will point to 5, so head always points to the LRU element, and tail to the MRU element. When the cache is full and we want to drop the LRU element, we simply lookup the dlist's head, drop that key from the map and the dlist. Note how we were able to find the LRU element in constant time. Dropping head is also a constant time operation. We couldn't have done this with only a map. Below statement follows from this:

> Statement 2: Finding the LRU element is `O(1)`. Dropping it from dlist and the map is also `O(1)` each.

Now let's see the complexity for maintaining this dlist. Let's consider the same access pattern as before = `1,2,3,4,5`. Now, what happens if 3 is accessed again? 3 has to move to the tail of the dlist because it is now the MRU element. The new dlist should be `1,2,4,5,3`. We want this operation to also be `O(1)`. If we traverse the list to find node 3 and then remove it, it would be `O(n)` complexity. To avoid this, we store the dlist's node in the map itself. For example, the map would look like this:
```
{
    key1 : (value1, Node(key1)), 
    key2 : (value2, Node(key2))
}
```
Each key stores a tuple - the value and its corresponding node in the dlist. This way, when a key is accessed, we immediately have access to the corresponding dlist node. Since its doubly-linked, we can alter the `next` and `prev` pointers of the node itself, its previous and next nodes to move the node to the tail in constant time. This is again `O(1)`. Remember we assumed a pre-existing element was accessed for this example? What if a non-existing element was accessed? In this case, if it was a read operation, the map returns -1 in `O(1)` time and dlist doesn't need modification. If it was a write operation, we simply have to make this element the new tail in our dlist, which is `O(1)`. And if this makes the dlist larger than `_MAX_SIZE`, we also drop the element at head. This is also `O(1)`.

>Statement 3: All 3 operations used to maintain the doubly-linked list are `O(1)` - updating tail, updating head, moving a element to the tail.

Now let's see each scenario and its time complexity:

**Scenario 1: Read a non-existing key**

The map immediately returns -1, hence its `O(1)`

**Scenario 2: Read an existing key**

The map gives the value and its corresponding dlist node in `O(1)`(from statement 1).   
Using this node reference we move the key in the dlist to the tail in `O(1)` (from statement 3)

**Scenario 3: Rewrite an existing key**

Value is stored in map and corresponding node is retrieved in `O(1)` (from statement 1).  
Using this node reference we move the key in the dlist to the tail in `O(1)` (from statement 3)

**Scenario 4: Write new key (cache is full)**

LRU element is looked up and dropped from the map and dlist in `O(1)` (from statement 2)  
A new node is created and appended to dlist's tail in `O(1)` (from statement 3)  
Value and node reference is stored in map in `O(1)`. (from statement 1)

**Scenario 5: Write new key (cache is not full)**

A new node is created and appended to dlist's tail in `O(1)` (from statement 3)  
Value and node reference is stored in map in `O(1)` (from statement 1).

## Space complexity

This implementation uses a map and a doubly linked list. If the size of the cache is `n`, then at any time, neither the map nor the list can have more than `n` elements. So we need `2n` space in worst case. In other words, the space complexity is `O(n)`.

## References
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)  
[Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)