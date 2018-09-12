import random

import matplotlib.pyplot as plt

from collections import defaultdict




class TreapNode(object):
    '''
    A node of a Treap (priority is determined at random and used to balance the Treap)
    '''
    def __init__(self, key, data=None):
        self.key = key
        self.priority = random.random()
        self.data = data
        self.parent = None
        self.left = None
        self.right = None

    def left_rotation(self):
        '''
        Perform a left rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        :return:
        '''
        root = self
        pivot = root.right
        root.right = pivot.left
        pivot.left = root
        root = pivot
        return root

    def right_rotation(self):
        '''
        Perform a right rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        :return:
        '''
        root = self
        pivot = root.left
        root.left = pivot.right
        pivot.right = root
        root = pivot
        return root

    def _search(self, key):
        '''
        Binary search the key in the Treap
        :param key:
        :return:
        '''
        current_node = self
        while current_node:
            if current_node.key == key:
                return current_node
            if key > current_node.key:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return False


    def __repr__(self, depth=0, left_offset=0, right_offset=0):
        ret = "\t"*depth+"node : "+repr(self.data)+" key : "+repr(self.key)+" priority : "+repr(self.priority)+"\n"
        if self.right:
            ret += "Right "+self.right.__repr__(depth=depth+1,right_offset=right_offset+1,left_offset=left_offset)
        if self.left:
            ret += "Left "+self.left.__repr__(depth=depth+1, left_offset=left_offset+1,right_offset=right_offset)
        return ret


class Treap(object):
    '''
    Data Structure that combine a tree and a heap
    https://gist.github.com/irachex/3922705
    see also : https://pypi.org/project/treap/1.39/
    '''
    def __init__(self,root=None):
        self.root = root

    def search(self, key):
        return self.root._search(key)

    def search_set(self,A):
        for i in A:
            if self.search(i):
                continue
            else:
                return False
        return True

    def insert(self, key, data=None, priority = False):
        self.root = self._insert(self.root,key,data,priority)

    def _insert(self,node,key,data,priority):
        if node is None:
            node = TreapNode(key, data)
            if priority:
                node.priority = priority
            return node

        if key < node.key:
            node.left = self._insert(node.left, key, data,priority)
            if node.left.priority < node.priority:
                node = node.right_rotation()

        elif key >= node.key:
            node.right = self._insert(node.right, key, data,priority)
            if node.right.priority < node.priority:
                node = node.left_rotation()
        return node

    def _balance(self,node):
        if node.left:
            node.left = self._balance(node.left)
            if node.left.priority < node.priority:
                node = node.right_rotation()
        if node.right:
            node.right = self._balance(node.right)
            if node.right.priority < node.priority:
                node = node.left_rotation()
        return node

    def balance(self):
        self.root = self._balance(self.root)

    def remove(self, key):
        self.root =self._remove(self.root,key)

    def _remove(self,node,key):
        if node.key == key:
            if not node.left and not node.right:
                return None
            elif not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                if node.left.priority < node.right.priority:
                    node = node.right_rotation()
                    node.right = self._remove(node.right, key)
                else:
                    node = node.left_rotation()
                    node.left = self._remove(node.left, key)
        elif key < node.key:
            node.left = self._remove(node.left, key)
        else:
            node.right = self._remove(node.right, key)
        return node

    def __repr__(self):
        return str(self.root)

    def _split_on_key(self,node,key):
        N = self._insert(node,key,data=None,priority=1*(10**-9))
        return N.left,N.right

    def split_on_key(self,key):
        L,R = self._split_on_key(self.root,key)
        return Treap(L),Treap(R)

    def get_max_value(self):
        current_node = self.root
        while current_node:
            max_value = current_node.key
            current_node = current_node.right
        return max_value

    def get_min_value(self):
        current_node = self.root
        while current_node:
            min_value = current_node.key
            current_node = current_node.left
        return min_value

    def reroot(self,key):
        N = self.search(key)
        N.priority = 1*(10**-9)
        self.balance()
        N.priority = random.random()

    def releaf(self,key):
        N = self.search(key)
        N.priority = 1
        self.balance()
        N.priority = random.random()

    def _get_data_in_key_order(self, node, L):
        if node:
            L.append((node.key,node.data))
        if node.right:
            self._get_data_in_key_order(node.right, L)
        if node.left:
            self._get_data_in_key_order(node.left, L)


    def get_data_in_key_order(self):
        L = []
        self._get_data_in_key_order(self.root, L)
        L.sort()
        return [i[1] for i in L]

def merge_treap(T1,T2):
    min_t1,min_t2 = T1.get_min_value(),T2.get_min_value()
    if min_t1 < min_t2:
        Tmin = T1
        max_Tmin = Tmin.get_max_value()
        Tmax = T2
        min_Tmax = min_t2
    else:
        Tmax = T1
        min_Tmax = min_t1
        Tmin = T2
        max_Tmin = Tmin.get_max_value()
    N = TreapNode(key =(min_Tmax+max_Tmin)/2)
    N.priority = 1
    N.left = Tmin.root
    N.right = Tmax.root
    ET = Treap(N)
    ET.balance()
    ET.remove(key = (min_Tmax+max_Tmin)/2)
    ET.balance()
    return ET


def union_treaps(T1,T2):
    '''
    Merge Tree T1 and T2
    :param T1: A Tree
    :param T2: A Tree
    :return:
    '''
    return Treap(_union_treaps(T1.root,T2.root))

def _union_treaps(N1, N2):
    if not N1:
        return N2
    if not N2:
        return N1
    if N1.priority < N2.priority:
        N1, N2 = N2, N1
    TN2 = Treap(N2)
    t_left,t_right = TN2._split_on_key(TN2.root,N1.key)
    N = TreapNode(key=N1.key,data=N1.data)
    N.priority = N1.priority
    N.left = _union_treaps(N1.left, t_left)
    N.right = _union_treaps(N1.right, t_right)
    return N




# if __name__ == '__main__':
#     E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6),(3,4)]
#     Data = {0:[0,1,2,3],
#             1:[0,4,5,8],
#             2:[],
#             3:[8,9,10,11],
#             4 :[],5:[],6:[]}




