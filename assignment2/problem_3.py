import heapq
from collections import deque

class Node:
    """
    Each node represents a node in the huffman tree. It stores the binary bit for itself and a reference to the parent node.
    """
    def __init__(self, char = None, freq = None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.parent = None
        self.bin = None

    def __repr__(self):
        return f"Node[{self.char}, {self.freq}, {self.bin}, left={self.left}, right={self.right}]"

class NodesHeap:
    """
    This class represents a heap that is specifically applicable for the huffman tree.
    """
    def __init__(self):
        self.nodes = []
        self.id = 0
        heapq.heapify(self.nodes)

    def push(self, node: Node):
        """
        Python's heap needs comparable values to operate, so we cannot just stuff a node inside it.
        Instead we use a tuple such as (node's frequency, unique id, node)

        See section "NodesHeap" in explanation for details.
        """
        heapq.heappush(self.nodes, (node.freq, self.id, node))
        self.id += 1

    def pop(self) -> Node:
        return heapq.heappop(self.nodes)[2] # We return the third value of the tuple because thats where we saved the node reference when it was pushed.

    def __repr__(self):
        return str(self.nodes)

    def __str__(self):
        return str(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)


def build_huffman_tree(input, debug = False):
    if len(input) == 0:
        return (None, None)

    freq_table = dict()
    for char in input:
        freq_table[char] = freq_table.get(char, 0) + 1

    if debug: print(f"frequency table: {freq_table}")
    nodes_heap = NodesHeap()
    leaf_nodes = dict()
    for char, freq in freq_table.items():
        node = Node(char=char, freq=freq)
        nodes_heap.push(node)
        leaf_nodes[char] = node

    if len(nodes_heap) == 1:
        node = nodes_heap.pop()
        node.bin = "0"
        nodes_heap.push(node)
    else:
        while len(nodes_heap) > 1:
            first_min = nodes_heap.pop()
            second_min = nodes_heap.pop()

            if debug: print(f"Heap after two pops: {nodes_heap}")
            first_min.bin = "0"
            second_min.bin = "1"

            parent = Node()
            parent.freq = first_min.freq + second_min.freq
            parent.left = first_min
            parent.right = second_min
            first_min.parent = parent
            second_min.parent = parent
            if debug: print(f"Parent node created: {parent}")
            nodes_heap.push(parent)

    if debug: print(f"Huffman tree: {nodes_heap}")
    if debug: print(f"Leaf nodes: {leaf_nodes}")
    return (nodes_heap.pop(),leaf_nodes)

def encode (input, leaf_nodes, debug=False):
    if len(input) == 0: return ""

    char_encoded_map = dict()
    encoded = []
    for char in input:
        #We first ensure we haven't already encoded char. No need to walk the tree if we have.
        if char not in char_encoded_map.keys():
            if debug: print(f"Encoding character {char}")

            # Since we have a reference to the leaf nodes, getting a reference to any leaf is a constant time operation.
            node = leaf_nodes[char]
            if debug: print(f"Leaf node for {char}: {node}")

            char_encoded = deque()
            # Root node doesn't have a bin value. We walk up the tree till we reach the root. In the special case where the root is also a leaf, it will have a bin value. In this case, its parent will become none after 1 iteration and the loop ends.
            while node is not None and node.bin:
                # We use the bits in the reverse order, so we append to th left
                char_encoded.appendleft(node.bin)
                node = node.parent
            char_encoded_map[char] = "".join(char_encoded)
        
        encoded.append(char_encoded_map[char])
            
    return "".join(encoded)

def decode (encoded, huffman_root: Node, debug=False) :
    if len(encoded) == 0: return ""

    decoded = []
    encoded_deque = deque(encoded)
    while len(encoded_deque) > 0:
        node = huffman_root
        
        if node.char is not None: # Only leaf nodes have a char value. If the root is also a leaf node, then we have only character in the tree and we already reached it
            encoded_deque.popleft()
        else:
            while node.char is None: # Only leaf nodes have a char value. We move downwards till we hit a leaf.
                bit = encoded_deque.popleft()
                if bit == "0": # Move left if we see 0
                    node = node.left
                else: # Move right if we see 1
                    node = node.right
        # When we reach a leaf node, we have successfully decoded a character

        #We use the char value of the leaf node that we reached at in the above steps.
        decoded.append(node.char)


    return "".join(decoded)

def test(input, expected_encoding, debug=False):
    huffman_root, leaf_nodes = build_huffman_tree(input, debug)
    
    actual_encoded = encode(input, leaf_nodes, debug)
    
    print(f"----------Input: {input}----------")
    print("Testing Status: ", end="")
    if actual_encoded == expected_encoding:
        print(f"Encoding pass.", end="")
    else:
        print(f"Encoding fail. Expected: {expected_encoding}, Actual: {actual_encoded}", end="")

    actual_decoded = decode(actual_encoded, huffman_root, debug)
    
    if actual_decoded == input:
        print(f" Decoding pass.")
    else:
        print(f"Decoding fail. Expected: {input}, Actual: {actual_decoded}")

    if len(input) > 0:
        #Assuming Unicode encoding, which needs 16 bits per character
        bits_before_compression = len(input) * 16 
        bits_after_decompression = len(actual_decoded) * 16

        #Each character in the string is a bit. So the length will give us the number of bits. This will be the size of data we transmit in terms of bits
        bits_after_compression = len(actual_encoded)
        print(f"Size (number of bits) before compression: {bits_before_compression}")
        print(f"Size (number of bits) after compression: {bits_after_compression}")
        print(f"Size (number of bits) after decompression: {bits_after_decompression}")
        print(f"Compression: {100 - (bits_after_compression / bits_before_compression) * 100}%")


test("AAAAAAABBBCCCCCCCDDEEEEEE", "1010101010101000100100111111111111111000000010101010101")
test("AAABBC", "000111110")
test("A", "0")
test("AB", "01")
test("", "")
test("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0110001101011100111110000100011001010011101001010110110101111100011001110101101111100111011111011111000000010010001101000101")