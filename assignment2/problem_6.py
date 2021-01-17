class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)
    
class LinkedListSet:
    def __init__(self):
        self.unique_elements = set()
        self.head = None

    def __str__(self):
        return " -> ".join(map(str,self))

    def __iter__(self):
        self.iter_cur_node = self.head
        return self

    def __next__(self):
        if self.iter_cur_node is None:
            raise StopIteration
        next_value = self.iter_cur_node.value
        self.iter_cur_node = self.iter_cur_node.next
        return next_value

    def __contains__(self, item):
        return item in self.unique_elements

    def append(self, value):
        if value in self.unique_elements:
            return

        self.unique_elements.add(value)

        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        new_node.next = self.head
        self.head = new_node

    def size(self):
        return len(self.unique_elements)

    def to_list(self):
        return [value for value in self]

def union(llist_1, llist_2):
    union_list = LinkedListSet()

    for each_list in [llist_1, llist_2]:
        for value in each_list:
            union_list.append(value)

    return union_list

def intersection(llist_1, llist_2):
    intersection_list = LinkedListSet()

    for value in llist_1:
        if value in llist_2:
            intersection_list.append(value)

    return intersection_list
        
def test(list1, list2, expected_list, operation, debug=False):
    llist1 = LinkedListSet()
    llist2 = LinkedListSet()

    for value in list1:
        llist1.append(value)

    for value in list2:
        llist2.append(value)

    if operation == "union" :
        assert sorted(union(llist1, llist2).to_list()) == sorted(expected_list)
        if debug: print(f"Expected: {expected_list}. Actual: {union(llist1, llist2).to_list()}")
    elif operation == "intersection":
        assert sorted(intersection(llist1, llist2).to_list()) == sorted(expected_list)
        if debug: print(f"Expected: {expected_list}. Actual: {intersection(llist1, llist2).to_list()}")
    else:
        raise Exception("Operation not recognized")

    
    
#Test case 1: Union of 2 empty llists is an empty list
test([],[],[],"union")

#Test case 2: Intersection of 2 empty llists is an empty list
test([],[],[],"intersection")

#------------------------------------------------------------------------

#Test case 3: Union of two lists with one distinct element each
test([1],[2],[1,2],"union")

#Test case 4: Intersection of two lists with one distinct element each
test([1],[2],[],"intersection")

#------------------------------------------------------------------------

#Test case 5: Union of two lists with several distinct elements each
test([1,2,3,4],[5,6,7],[1,2,3,4,5,6,7],"union")

#Test case 6: Intersection of two lists with several distinct elements each
test([1,2,3,4],[5,6,7],[],"intersection")

#------------------------------------------------------------------------

#Test case 7: Union of two lists with overlapping elements without duplicate elements in a list
test([1,2,3,4,5],[3,4,5,6,7],[1,2,3,4,5,6,7],"union")

#Test case 8: Intersection of two lists with overlapping elements without duplicate elements in a list
test([1,2,3,4,5],[3,4,5,6,7],[5,4,3],"intersection")

#------------------------------------------------------------------------

#Test case 9: Union of two lists with overlapping elements with duplicate elements in a list
test([1,1,2,3,4,5,5],[3,3,4,5,6,6,7],[1,2,3,4,5,6,7],"union")

#Test case 10: Intersection of two lists with overlapping elements with duplicate elements in a list
test([1,1,2,3,4,5,5],[3,3,4,5,6,6,7],[5,4,3],"intersection")