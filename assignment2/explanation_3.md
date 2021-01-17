# Huffman Tree

This document explains the requirements for the problem and design decisions behind the solution in `problem_3.py` file.

## Requirements

1. Construct the huffman tree for a given input string.
2. Encode the input using the huffman tree.
3. Decode the encoded data from step 2 using the huffman tree.
4. Test if the input and decoded data from step 3 are same.

## Algorithm Breakdown (with design decisions)
The algorithm depends on a couple of abstract data types - `Node` and `NodesHeap`.

### Node
An object from this class represents a node in the huffman tree. Below are its properties:
* The huffman tree is a binary tree, so we have `left` and `right` properties.
* We need to traverse the tree bottom-up when encoding. So each node stores a reference to its parent, called `parent`.
* `char` is the character represented by the node.
* `freq` is the frequency of occurrence of the corresponding character. In case of nodes which don't represent a character, this value is the combined frequencies of its children characters.
* `bin` is either `0` or `1`. If the node is a left child, its set to `1`, `0` if a right child. This is used when encoding and decoding

The node itself is unware of the roles of each property. The huffman tree generation logic uses these properties according to these rules.

### NodesHeap
We use a heap because we need the node with lowest frequency at each step when generating the tree. Heap allows us to do that in `O(log n)` time.

This class makes it easier to store nodes in a heap. It encapsulates python's `heapq` usage to make it seem that we're directly pushing and popping nodes from this heap. This makes the caller's code cleaner.

The `push` method accepts objects of type `Node`, and the `pop` method returns an object of the same type. However, the actual heap data looks like below:
```
0: (45, 0, node:Node)
1: (23, 1, node:Node)
2: (11, 2, node:Node)
3: (21, 3, node:Node)
```
These are tuples, the first value being the node's frequency, second being a incremental counter, third being the actual nodes that were pushed on the heap. Python uses the first value of the tuple for comparison, which is an integer. When the first value of two tuples are same, the heap will compare the next counter value of the tuple. Since this is alway unique, any tie is broken at random. This is okay because the algorithm works the same either way. We use this approach because Python's heapify will not work on non-comparable values and objects from a custom class are non-comparable.

### Building the Tree (with time complexity)
**Step 1: Generate Frequency Table** We first look through each character and generate a map that maps characters to their frequency of occurrence in the input string. This is `O(n)` since we look each element once.

**Step 2: Generate leaf nodes and store in heap** We look through the characters in the map and create a leaf node for each character. In the worst case, all characters are unique and we generate `n` leaf nodes. We push each leaf node into an heap, which is a `O(log n)` operation each. Overall, this is `O(n log n)`.

**Step 3: Generate all internal nodes** For every node in the heap, we iteratively perform the below steps until we have a single node in the heap:
1. Remove 2 nodes with minimal frequencies. Removing from a heap is `O(log n)`. This is overall `O(2 log n)` since we remove 2 nodes.
2. Generate a parent node with appropriate values. The values are listed in "Node" section above. This is `O(1)`
3. Push the parent node on to the heap. This is `O(log n)`.

These 3 steps repeat for every node, which is `n` times. This is because the number of nodes reduces by 1 in every iteration and we started off with `n` nodes.

So overall, this is `O(n (2 log n + 1 + log n))`. By simplifying and dropping the lower order terms, the complexity for step 3 is `O(n log n)`.

All 3 steps put together is `O(n + n log n + n log n)`, since they happen one after the other. Again, by dropping lower order terms, the overall complexity for generating the huffman tree is `O(n log n)`

### Encoding

For encoding we start at a character (a leaf node) and walk up to the root. This path gives us a stream of bits. Reversing this stream gives us the encoding for that character. For this reason, we track the leaf nodes in a map, `leaf_nodes`. That way, we can immediately find the leaf node for a character and start encoding it. Repeating this for every character gives us the encoded value. We also maintain a map of characters to their encoding, `char_encoded_map`. This map acts as a cache, so we don't have to encode the same character more than once. If encoded once, we can reuse it from this map.

### Decoding

For decoding, we start at the root of the huffman tree and walk downwards until we reach a leaf, following the path of the decoded bits. We move left when we see a `0` and right when we see a `1`. We also pop the bits from the stream as we move. This way, we know when the input stream ends. We pick the `char` value of the leaf node and append it to `decoded` list.

### Time complexity for encoding and decoding

For encoding, we walk up the tree. For decoding, we walk down the tree. Thus, both operations depend on the height of the tree. Let's say the height is `h`.

While encoding, we walk the tree once for each character we see. We already said `n` is the number of characters. Thus, we walk a tree of height `h`, `n` times. This is `O(hn)`.

While decoding, we walk the tree once for each bit we see. Even though we do not walk the full height of the tree for every bit we see, we do walk the full tree for every character we decode, which will be `n`. So this is again `O(nh)`.

Now, `h` is the height of the tree, but what is it's relationship with the input size, `n`? We need to establish this relationship because time complexity must be in terms of the input size. In the worst case, the height of the tree will be `n`. This happens when the frequency of the characters forms a fibonacci sequence. For such an input, each character will contribute to the height of the tree and `h` becomes equal to `n`. This makes the complexity `O(n squared)`.

However, in the practical world, huffman trees are mostly generated beforehand and both encoding and decoding parties have a reference to it. The huffman trees are generated by sampling a huge data set. At this stage, we can also make adjustments to the frequencies to make the tree balanced. Moreover, the chances of a fibonacci series of frequencies is impossible for any practical data set - english, computer programs etc. Given these considerations, we can ensure a nearly balanced huffman tree, in which case the height will equal `log n`. So for any practical use cases, we can say the complexity for encoding and decoding is `n log n`.

As we encode and decode, we maintain two lists - one tracks the data processed so far, another the data yet to be processed. The complexity for this is `O(1)` because we either append/pop to/from the left or right as we go. We can ignore this since its a constant time operation. After building the list, we iterate the list once to get the final encoded/decoded data. This is `O(n)`. We can ignore this because its a lower order term compared to `n log n`.

## Space complexity
We have `n` characters to encode. In worst case, we end up with `n` leaf nodes for the huffman tree. When generating the huffman tree, we pop 2 nodes and insert 1 node in each step from the heap. This can at most generate `2n` nodes. When encoding and decoding we maintain 2 lists to track the data processed so far, and the data yet to be processed. This is `4n` - 2 lists of size `n` when encoding, and 2 lists when decoding. Overall, space complexity is `O (2n + 4n)`. After simplification and dropping lower order terms, this is `O(n)`.

## Summary
* Worst-case time complexity for generating the huffman tree is `O(n log n)`.
* Worst-case time complexity for encoding and decoding is `O(n squared)`. However, we can ensure a balanced tree for practical data sets. So we can consider the actual complexity to be `O (n log n)`
* There are additional lists to be maintained during encoding and decoding. These are mostly constant time operations and one time iterations. We ignore them because they are lower order terms.
* The space complexity is `O (n)` for generating the tree, encoding and decoding put together.
  
## References
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)  
[Efficient way to join strings](https://stackoverflow.com/a/1316959/5800527)  
[Huffman Coding Visualization](https://people.ok.ubc.ca/ylucet/DS/Huffman.html)  
[Using Tuples In Heap](https://stackoverflow.com/a/8875823/5800527)  
[Heap queue (or heapq) in Python](https://www.tutorialspoint.com/heap-queue-or-heapq-in-python)  
[Huffman tree time complexity](https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html#:~:text=The%20time%20complexity%20of%20the,iterations%2C%20one%20for%20each%20item.)  
[Max height of huffman tree](https://stackoverflow.com/questions/28767144/huffman-tree-with-max-height-nice-questions)