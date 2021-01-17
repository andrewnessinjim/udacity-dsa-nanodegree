import hashlib
from datetime import timezone, datetime

class Block:
    def __init__(self, data, prev_hash=None):
        self.data = data
        self.timestamp = datetime.now(timezone.utc)
        self.prev_hash = prev_hash
        self.hash = self._calculate_hash()
        self.prev = None
        self.next = None

    def _calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((self.data + str(self.timestamp) + str(self.prev_hash)).encode("utf-8"))
        return sha.hexdigest()
    
    def __repr__(self):
        return "\n".join(
            ["Data: " + self.data, 
            "Created time: " + str(self.timestamp) ,
            "Hash:" +self.hash,
            "Previous hash: " + str(self.prev_hash),
            "---------",
            ""])


class BlockChain:
    """
    This class uses a doubly linked list to store the blocks. This makes retrieval of a
    particular block O(n). Using an array can avoid this. But the problem statement does 
    not require us to retrieve a particular block and requires the use of a linked list.
    """
    def __init__(self):
        # Tracking head is optional. Its used here for the convenience of retrieving blocks in the order they were inserted.
        self.head = None 
        self.tail = None

    def _add_block(self,newBlock:Block):
        if self.tail is None:
            self.tail = newBlock
            self.head = newBlock
            return
        
        newBlock.prev_hash = self.tail.hash
        newBlock.prev = self.tail
        self.tail.next = newBlock
        self.tail = newBlock

    def add_data(self, data):
        if(self.tail):
            self._add_block(Block(data, self.tail.hash))
        else:
            self._add_block(Block(data))

    def __repr__(self):
        output = ""
        cur_node = self.head
        while cur_node:
            output += str(cur_node)
            cur_node = cur_node.next

        return output

    def is_valid(self):
        cur_block = self.tail
        while cur_block:
            if cur_block.hash != cur_block._calculate_hash():
                return False
            
            prev_block:Block = cur_block.prev
            if prev_block:
                if cur_block.prev_hash != prev_block.hash:
                    return False

            cur_block = prev_block

        return True


"""
Test case 1: A chain with zero blocks is valid
"""
no_blocks = BlockChain()
no_blocks.add_data("Andrew")
assert no_blocks.is_valid()

"""
Test case 2: A chain with one element is valid when there is no tampering
"""
one_block_tamper = BlockChain()
one_block_tamper.add_data("Andrew")
assert one_block_tamper.is_valid()

"""
Test case 3: A chain with several elements is valid when there is no tampering
"""
several_blocks_no_tamper = BlockChain()
several_blocks_no_tamper.add_data("Nessin")
several_blocks_no_tamper.add_data("Data Structures")
several_blocks_no_tamper.add_data("Udacity")
several_blocks_no_tamper.add_data("Algorithms")
several_blocks_no_tamper.add_data("Simple Blockchain")
assert several_blocks_no_tamper.is_valid()

"""
Test case 4: A chain with one element is invalid when data is tampered after creation
"""
one_block_tamper = BlockChain()
one_block_tamper.add_data("Andrew")
one_block_tamper.head.data = "Tampered Andrew"
assert one_block_tamper.is_valid() == False

"""
Test case 5: A chain with several elements is invalid when data of any block is tampered after creation
"""
several_blocks_no_tamper = BlockChain()
several_blocks_no_tamper.add_data("Nessin")
several_blocks_no_tamper.add_data("Data Structures")
several_blocks_no_tamper.add_data("Udacity")

random_block = several_blocks_no_tamper.head.next
random_block.data = "tampered Data Structures"

assert several_blocks_no_tamper.is_valid() == False

"""
Test case 5: A chain with several elements is invalid when data is tampered after creation, and hashcode for that block is recalculated. The current is_valid() implementation does not work if tail of the blockchain is tampered this way. Such tampering can be detected and corrected in a distributed environment where each node communicates with each other to reach a consensus on the valid blocks.
"""
several_blocks_tamper = BlockChain()
several_blocks_tamper.add_data("Nessin")
several_blocks_tamper.add_data("Data Structures")
several_blocks_tamper.add_data("Udacity")

random_block = several_blocks_tamper.head.next
random_block.data = "tampered Data Structures"
random_block.hash = random_block._calculate_hash()

assert several_blocks_tamper.is_valid() == False