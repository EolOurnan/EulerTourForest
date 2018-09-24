import random

import matplotlib.pyplot as plt
import matplotlib.collections as mcol

from collections import defaultdict


class TreapNode(object):
    '''
    A node of a Treap (priority is determined at random and used to balance the Treap)
    '''

    def __init__(self, key, data=None):
        '''

        :param key:
        :param data:
        '''
        self.key = key
        self.priority = random.random()
        self.data = data
        self.parent = None
        self.left = None   # Left child
        self.right = None  # Right child
        self.pred = None   # Predecessor (used in euler tour tree, flemme d'hériter)
        self.suc = None    # successor (used in euler tour tree, flemme d'hériter)

    def left_rotation(self):
        '''
        Perform a left rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't chang ethe cyclic order, successor and predecessor unchanged
        :return:
        '''
        root = self
        pivot = root.right

        # Change filiation
        if self.parent:
            pivot.parent = root.parent
            root.parent = pivot
            if pivot.left:
                pivot.left.parent = root

        # Rotate
        root.right = pivot.left
        pivot.left = root
        root = pivot
        return root

    def right_rotation(self):
        '''
        Perform a right rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't chang ethe cyclic order, successor and predecessor unchanged
        :return:
        '''
        root = self
        pivot = root.left

        # Change filiation
        if self.parent:
            pivot.parent = root.parent
            root.parent = pivot
            if pivot.right:
                pivot.right.parent = root

        # Rotate
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

        # print(" depth : ",depth," right offset : ",right_offset," left offset : ",left_offset)
        ret = "\t" * depth
        if self.parent:
            ret += " parent key : " + repr(self.parent.key)
        if self.suc:
            ret += " | suc key : " + repr(self.suc.key)
        if self.pred:
            ret += " | pred key : " + repr(self.pred.key)

        ret += " | node : " + repr(
            self.data) + " key : " + repr(self.key) + " priority : " + repr(
            self.priority) + "\n"

        if self.right:
            ret += "Right " + self.right.__repr__(depth=depth + 1, right_offset=right_offset + 1,
                                                  left_offset=left_offset)
        if self.left:
            ret += "Left " + self.left.__repr__(depth=depth + 1, left_offset=left_offset + 1,
                                                right_offset=right_offset)
        return ret


class Treap(object):
    '''
    Data Structure that combine a tree and a heap
    https://gist.github.com/irachex/3922705
    see also : https://pypi.org/project/treap/1.39/
    '''

    def __init__(self, root=None, first = None, last = None):
        '''
        :param root: Root of the Treap (a TreapNode)
        :param first: First node of Euler Tree
        :param last:  Last node of Euler Tree
        '''
        self.root = root
        self.first = first
        self.last = last

    def __repr__(self):
        return str(self.root)

    def first(self):
        return self.first

    def last(self):
        return self.last

    def plot(self, title=None):
        N, E = self.get_internal_structure()
        fig, ax = plt.subplots()
        y_min = 0
        x_min = 0
        x_max = 0
        # Nodes are ordered as in a DFS traversal of the tree
        for pos, data in N:
            label = str(data[0]) + "\n"+ str(data[1]) #+"\n"+str(data[2])  #priority
            x_max = max(x_max, pos[0])
            x_min = min(x_min, pos[0])
            y_min = min(y_min, pos[1])
            ax.text(pos[0], pos[1], label, color='#2d5986',
                    bbox=dict(facecolor='none', edgecolor='#2d5986', boxstyle='round,pad=1'))

        # Set limit
        edge_collections = mcol.LineCollection(E, colors=['#2d5986'])

        ax.add_collection(edge_collections)
        ax.set_ylim(y_min - 1, 1)
        ax.set_xlim(x_min - 1, x_max + 1)
        if title:
            ax.set_title(title)

    def check_tree_invariant(self):
        '''
        Check the tree invariant of the Treap
        :return: True if invariant respected, false otherwise
        '''
        return self._check_tree_invariant(self.root)

    def _check_tree_invariant(self, node):
        if node.left:
            assert node.key > node.left.key
            assert self._check_tree_invariant(node.left)
        if node.right:
            assert node.key < node.right.key
            assert self._check_tree_invariant(node.right)
        return True

    def check_heap_invariant(self):
        '''
        Check the heap invariant of the Treap
        :return: True if invariant respected, false otherwise
        '''
        return self._check_heap_invariant(self.root)


    def _check_heap_invariant(self, node):
        if node.left:
            assert node.priority <= node.left.priority
            assert self._check_tree_invariant(node.left)
        if node.right:
            assert node.priority <= node.right.priority
            assert self._check_tree_invariant(node.right)
        return True

    def check_invariants(self):
        '''
        Check the two invariants of the Treap :
        - Heap invariant
        - (Binary) Tree invariant
        :return: True if invariants respected, false otherwise
        '''
        assert self.check_tree_invariant()
        assert self.check_heap_invariant()

    def search(self, key):
        '''
        Search a key in the Treap $O(log(n))$
        :param key: The key to query
        :return: The Node with the corresponding key
        '''
        return self.root._search(key)

    def search_set(self, A):
        for i in A:
            if self.search(i):
                continue
            else:
                return False
        return True

    def swap_data(self,u,v):
        u.data,v.data = v.data,u.data


    def swap_nodes(self, u, v):
        # Swap priorities
        u.priority, v.priority = v.priority, u.priority

        # Swap parents
        if u.parent:
            if u.parent.left == u:
                u.parent.left = v
            else:
                u.parent.right = v
        if v.parent:
            if v.parent.left == v:
                v.parent.left = u
            else:
                v.parent.right = u
        u.parent, v.parent = v.parent, u.parent

        # Swap left child
        if u.left:
            u.left.parent = v
        if v.left:
            v.left.parent = u
        u.left, v.left = v.left, u.left

        # Swap right child
        if u.right:
            u.right.parent = v
        if v.right:
            v.right.parent = u
        u.right,v.right = v.right,u.right

        # Eventually change suc and pred (TODO)
        # if u.suc:
        #     u.suc.pred = v
        # if v.suc:
        #     v.suc.pred = u
        # u.suc,v.suc = v.suc,u.suc
        #
        # if u.pred:
        #     u.pred.suc =v
        # if v.pred:
        #     v.pred.suc =u
        # u.pred,v.pred = v.pred,u.pred
        # Eventulally change #SIZE
        # u.size,v.size = v.size,u.size


    def get_internal_structure(self):
        return self._get_internal_structure(self.root)

    def _get_internal_structure(self, node, N=None, E=None, x_parent=0, y_parent=0):
        '''
        Return (x_pos,y_pos==depth)
        :param node:
        :param depth:
        :return:
        '''
        if not N:
            N = []
        if not E:
            E = []
        N.append(((x_parent, y_parent), (node.key, node.data))) #,node.priority))) # priority
        if node.left:
            if y_parent:
                y_pos = y_parent - 1
                offset = x_parent / y_pos
                if offset > 0:
                    x_pos = x_parent - offset
                else:
                    x_pos = x_parent + offset
            else:
                x_pos = -10
                y_pos = -1

            E.append(((x_parent, y_parent), (x_pos, y_pos)))
            self._get_internal_structure(node.left, N=N, E=E, x_parent=x_pos, y_parent=y_pos)
        if node.right:
            if y_parent:
                y_pos = y_parent - 1
                offset = x_parent / y_pos
                if offset > 0:
                    x_pos = x_parent + offset
                else:
                    x_pos = x_parent - offset
            else:
                x_pos = 10
                y_pos = -1
            E.append(((x_parent, y_parent), (x_pos, y_pos)))
            self._get_internal_structure(node.right, N=N, E=E, x_parent=x_pos, y_parent=y_pos)
        return N, E

    def insert(self, key, data=None, priority=False,
               suc =None,pred = None,inlast=False,infirst=False):
        '''
        Insert a node in the Treap
        :param key:
        :param data:
        :param priority:
        :param suc:
        :param pred:
        :return:
        '''
        self.root = self._insert(self.root, key=key,
                                 data= data, priority= priority,
                                 suc = suc, pred = pred)
        node = self.search(key)
        if inlast:       # It means that this node is the new last
            self.last.suc = node
            node.pred = self.last
            self.last = node
            self.last.suc = self.first
            self.first.pred = node
        elif infirst:
            self.first.pred = node
            node.suc = self.first
            self.first = node
            self.first.pred = self.last
            self.last.suc = node
        elif not pred and not suc:
            node.pred = self.predecessor(node)
            if node.pred:
                node.pred.suc = node
            else:
                self.first = node
                node.pred = self.last
            node.suc = self.successor(node)
            if node.suc:
                node.suc.pred = node
            else:
                node.suc = self.first
                self.last = node
                self.first.pred = node


    def _insert(self, node, key, data, priority, suc=None, pred=None, parent=None):
        if node is None:
            node = TreapNode(key, data)
            if priority:
                node.priority = priority
            if parent:
                node.parent = parent
            if suc:
                node.suc = suc
            if pred:
                node.pred = pred
            return node

        if key < node.key:
            node.left = self._insert(node.left, key, data, priority, suc, pred, node)
            if node.left.priority < node.priority:
                node = node.right_rotation()

        elif key >= node.key:
            node.right = self._insert(node.right, key, data, priority, suc, pred, node)
            if node.right.priority < node.priority:
                node = node.left_rotation()

        return node

    def _balance(self, node):
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
        '''
        Balance the Treap to respect the Heap invariant
        :return:
        '''
        self.root = self._balance(self.root)

    def predecessor(self, node):
        '''
        Find the predecessor of 'node' in the key ordering (biggest key smaller than node.key)
        :param node:
        :return:
        '''
        pred = None
        current = self.root
        if current is None:
            raise KeyError
        if node.left:
            node = self._find_max_node(node.left)
            return node
        while current:
            if node.key > current.key:
                pred = current
                current = current.right
            elif node.key < current.key:
                current = current.left
            else:
                break
        return pred

    def successor(self, node):
        '''
        Find the successor of 'node' in the key ordering (smallest key bigger than node.key)
        :param node:
        :return:
        '''
        succ = None
        current = self.root
        if current is None:
            raise KeyError
        if node.right:
            node = self._find_min_node(node.right)
            return node
        while current:
            if node.key < current.key:
                succ = current
                current = current.left
            elif node.key > current.key:
                current = current.right
            else:
                break
        return succ

    def remove(self, key):
        '''
        Remove the node corresponding to the key
        :param key: The key to remove
        :return:
        '''
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):

        def update(node):
            if node == self.first:
                self.first = node.suc
            if node == self.last:
                self.last = node.pred
            if node.pred:
                node.pred.suc = node.suc
            if node.suc:
                node.suc.pred = node.pred

        if node.key == key:
            if not node.left and not node.right:
                update(node)
                return None

            elif not node.left:
                update(node)
                if node.parent:
                    node.right.parent = node.parent
                return node.right

            elif not node.right:
                update(node)
                #Change filiation
                if node.parent:
                    node.left.parent = node.parent
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


    def _split_on_key(self, node, key):
        N = self._insert(node, key, data=None, priority=1 * (10 ** -9))
        return N.left, N.right

    def split_on_key(self, key):
        L, R = self._split_on_key(self.root, key)
        # Fixed pred and suc
        print("L key :", L.key)
        if L.pred and L.suc:
            if L.pred:
                print("L pred :",L.pred.key)
            if L.suc:
                print("L suc :",L.suc.key)
            L_first_node = self.first
            L_last_node = self._find_max_node(L)
            L_first_node.pred = L_last_node
            L_last_node.suc = L_first_node
        print("R key :", R.key)
        if R.pred and R.suc:
            if R.pred:
                print("R pred :",R.pred.key)
            if R.suc:
                print("R suc :",R.suc.key)
            R_first_node = self._find_min_node(R)
            R_last_node = self.last
            R_first_node.pred = R_last_node
            R_last_node.suc = R_first_node
        return Treap(L,first=L_first_node,last=L_last_node), Treap(R,first=R_first_node,last=R_last_node)

    def find_max_value(self):
        '''
        Find the maximum value in the Treap
        :return: Maximum value
        '''
        return self._find_max_value(self.root)

    def _find_max_value(self, node):
        '''
        Find the maximum value in the subtree rooted in :param node:
        :param node: Node to start search
        :return: Maximum key in subtree
        '''
        while node.right:
            node = node.right
        return node.key

    def find_min_value(self):
        '''
        Find the minimum value in the Treap
        :return: Minimum value
        '''
        return self._find_min_value(self.root)

    def _find_min_value(self, node):
        '''
        Find the minimum value in the subtree rooted in :param node:
        :param node: Node to start search
        :return: Minimum key in subtree
        '''
        while node.left:
            node = node.left
        return node.key

    def find_max_node(self):
        '''
        Find the maximum node in the Treap
        :return: Maximum node
        '''
        return self._find_max_node(self.root)

    def _find_max_node(self, node):
        '''
        Find the maximum node in the subtree rooted in :param node:
        :param node: Node to start search
        :return: Maximum node in subtree
        '''
        while node.right:
            node = node.right
        return node

    def find_min_node(self):
        '''
        Find the minimum node in the Treap
        :return: Minimum node
        '''
        return self._find_min_node(self.root)

    def _find_min_node(self, node):
        '''
        Find the minimum node in the subtree rooted in :param node:
        :param node: Node to start search
        :return: Minimum node in subtree
        '''
        while node.left:
            node = node.left
        return node

    def reroot(self, key):
        N = self.search(key)
        N.priority = 1 * (10 ** -9)
        self.balance()
        N.priority = random.random()
        # Also put in first position in euler tour
        self.first = N
        self.last = N.pred

    def releaf(self, key):
        N = self.search(key)
        N.priority = 1
        self.balance()
        N.priority = random.random()
        # Also put in last position in euler tour
        self.last = N
        self.first = N.suc

    def _get_data_in_key_order(self, node, L):
        if node:
            L.append((node.key, node.data))
        if node.right:
            self._get_data_in_key_order(node.right, L)
        if node.left:
            self._get_data_in_key_order(node.left, L)

    def get_data_in_key_order(self,with_key=None):
        L = []
        self._get_data_in_key_order(self.root, L)
        L.sort()
        if with_key:
            return L
        return [i[1] for i in L]

    def get_data_in_priority_order(self):
        L = []
        self._get_data_in_key_order(self.root, L)
        return [i[1] for i in L]


def merge_treap(T1, T2):
    '''
    Merge Treap from a former Split
    :param T1:
    :param T2:
    :return:
    '''
    min_t1, min_t2 = T1.find_min_value(), T2.find_min_value()
    if min_t1 < min_t2:
        Tmin = T1
        max_Tmin = Tmin.find_max_value()
        Tmax = T2
        min_Tmax = min_t2
    else:
        Tmax = T1
        min_Tmax = min_t1
        Tmin = T2
        max_Tmin = Tmin.find_max_value()
    N = TreapNode(key=(min_Tmax + max_Tmin) / 2)
    N.priority = 1
    N.left = Tmin.root
    N.right = Tmax.root
    ET = Treap(N)
    ET.balance()
    ET.remove(key=(min_Tmax + max_Tmin) / 2)
    ET.balance()
    return ET


def union_treaps(T1, T2):
    '''
    Merge Tree T1 and T2
    :param T1: A Tree
    :param T2: A Tree
    :return:
    '''
    # print("T1 first key :",T1.first.key)
    # print("T1 last key :",T1.last.key)
    # print("T2 first key :",T2.first.key)
    # print("T2 last key :",T2.last.key)
    # print("Union Treap:")
    # MIDDLE
    T1.last.suc = T2.first
    T2.first.pred = T1.last

    #BEGINNING
    T1.first.pred = T2.last

    #ENDING
    T2.last.suc = T1.first

    T = Treap(_union_treaps(T1.root, T2.root), first=T1.first, last=T2.last)
    # print("T first key :",T.first.key)
    # print("T last key :",T.last.key)
    return T


def _union_treaps(N1, N2):
    if not N1:
        return N2
    if not N2:
        return N1
    if N1.priority < N2.priority:
        N1, N2 = N2, N1
    TN2 = Treap(N2)
    t_left, t_right = TN2._split_on_key(TN2.root, N1.key)
    N = TreapNode(key=N1.key, data=N1.data)
    N.priority = N1.priority
    N.parent = N1.parent
    N.suc = N1.suc
    N.pred = N1.pred
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
