import random

import matplotlib.pyplot as plt
import matplotlib.collections as mcol


class CTreapNode(object):
    '''
    A node of a Treap (priority is determined at random and used to balance the Treap)
    '''

    def __init__(self, data=None, parent=None, pred=None, suc=None, size=None):
        '''

        :param value:
        :param data:
        '''
        self.data = data
        self.priority = random.random()
        self.parent = parent
        self.left = None  # Left child
        self.right = None  # Right child
        self.pred = pred  # Predecessor (used in Euler Tour)
        self.suc = suc  # successor   (used in Euler Tour
        self.size = size  # Used to count the number of nodes in the subtree rooted at the current node


    def find_root(self):
        '''
        Find the root of the current node
        :param node:
        :return:
        '''
        current = self
        while current.parent:
            current = current.parent
        return current

    def left_rotation(self):
        '''
        Perform a left rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't change the cyclic order, successor and predecessor unchanged
        :return: New root (aka the right child)
        '''
        root = self
        pivot = root.right

        # Change filiation
        pivot.parent = root.parent
        root.parent = pivot
        if pivot.left:
            pivot.left.parent = root

        # Change size
        root.size,pivot.size = pivot.size,root.size

        # Rotate
        root.right = pivot.left
        pivot.left = root
        root = pivot

        return root

    def right_rotation(self):
        '''
        Perform a right rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't change the cyclic order, successor and predecessor unchanged
        :return: New root ( aka the left child)
        '''
        root = self
        pivot = root.left

        # Change filiation
        pivot.parent = root.parent
        root.parent = pivot
        if pivot.right:
            pivot.right.parent = root

        # Change size
        root.size,pivot.size = pivot.size,root.size

        # Rotate
        root.left = pivot.right
        pivot.right = root
        root = pivot

        return root

    def update_size(self):
        '''
        Used to keep the size
        :param node:
        :return:
        '''
        c = 1
        if self.left:
            c += self.left.size
        if self.right:
            c += self.right.size
        self.size = c

    def clear(self):
        self.parent = None
        self.left = None
        self.right = None
        self.pred = None
        self.suc = None

    def __repr__(self, depth=0, left_offset=0, right_offset=0):

        # print(" depth : ",depth," right offset : ",right_offset," left offset : ",left_offset)
        ret = "\t" * depth
        if self.parent:
            ret += " parent data : " + repr(self.parent.data)
        if self.suc:
            ret += " | suc data : " + repr(self.suc.data)
        if self.pred:
            ret += " | pred data : " + repr(self.pred.data)

        ret += " | node data : " + repr(
            self.data) + " priority : " + repr(
            self.priority) + "\n"

        if self.right:
            ret += "Right " + self.right.__repr__(depth=depth + 1, right_offset=right_offset + 1,
                                                  left_offset=left_offset)
        if self.left:
            ret += "Left " + self.left.__repr__(depth=depth + 1, left_offset=left_offset + 1,
                                                right_offset=right_offset)
        return ret


class CTreap(object):
    '''
    Treap, binary randomized tree self balanced and key by index ( not a usual key)
    '''

    def __init__(self, root=None, first=None, last=None):
        '''
        :param root: Root of the Treap (a TreapNode)
        :param first: First node of Euler Tree
        :param last:  Last node of Euler Tree
        '''
        self.root = root
        self.first = first
        self.last = last

    def _get_data_in_priority_order(self, node, L):
        if node:
            L.append(node.data)
        if node.right:
            self._get_data_in_priority_order(node.right, L)
        if node.left:
            self._get_data_in_priority_order(node.left, L)

    def get_data_in_priority_order(self):
        L = []
        self._get_data_in_priority_order(self.root, L)
        return [i for i in L]

    def get_euler_tour(self):
        '''
        Return the induced euler tour representation of the Tree
        :return:
        '''
        first = self.first
        euler_tour = [first.data]
        current = first.suc
        # print("############################")
        # print("First :",self.tree.first.key)
        # print("Last :",self.tree.last.key)
        cnt =0
        while current != first:
            # if cnt >= 25:
            #     exit()
            # print("Current key :",current.key)
            euler_tour.append(current.data)
            current = current.suc
            cnt += 1
        return euler_tour

    def __repr__(self):
        rep = "Euler Tour : "+repr(self.get_euler_tour())+"\n"
        rep += " Priority Order :"+str(self.get_data_in_priority_order())+"\n"
        rep += +str(self.root)
        return rep

    def swap_nodes(self, u, v):
        u.priority, v.priority = v.priority, u.priority         # Swap priorities

        u.data, v.data = v.data, u.data         # Swap data

        u.size, v.size = v.size, u.size        # Swap size

        # Swap parents
        temp = u.parent
        u.parent = v.parent
        if v.parent:
            if v.parent.left == v:
                v.parent.left = u
            else:
                v.parent.right = u
        v.parent = temp
        if temp:
            if temp.left == u:
                temp.left = v
            else:
                temp.right = v

        # Swap left child
        temp = u.left
        u.left = v.left
        if v.left:
            v.left.parent = u
        v.left = temp
        if temp:
            temp.parent = v

        # Swap right child
        temp = u.right
        u.right = v.right
        if v.right:
            v.right.parent = u
        v.right = temp
        if temp:
            temp.parent = v

        # Swap suc
        temp = u.suc
        u.suc = v.suc
        if v.suc:
            v.suc.pred = u
        v.suc = temp
        if temp:
            temp.pred = v

        # Swap pred
        temp = u.pred
        u.pred = v.pred
        if v.pred:
            v.pred.suc = u
        v.pred = temp
        if temp:
            temp.suc = v

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
        N.append(((x_parent, y_parent), (node.data,node.size)))  # ,node.priority))) # priority
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

    def check_heap_invariant(self):
        '''
        Check the heap invariant of the Treap
        :return: True if invariant respected, false otherwise
        '''
        return self._check_heap_invariant(self.root)

    def _check_heap_invariant(self, node):
        if node.left:
            assert node.priority <= node.left.priority
            assert self._check_heap_invariant(node.left)
        if node.right:
            assert node.priority <= node.right.priority
            assert self._check_heap_invariant(node.right)
        return True

    def plot(self, title=None):
        N, E = self.get_internal_structure()
        fig, ax = plt.subplots()
        y_min = 0
        x_min = 0
        x_max = 0
        # Nodes are ordered as in a DFS traversal of the tree
        for pos, data in N:
            label = str(data[0])+ "\n" + str(data[1])  # Data + Size
            x_max = max(x_max, pos[0])
            x_min = min(x_min, pos[0])
            y_min = min(y_min, pos[1])
            ax.text(pos[0], pos[1], label, color='#2d5986',
                    bbox=dict(facecolor='none', edgecolor='#2d5986', boxstyle='round,pad=1'))

        # Set limit
        edge_collections = mcol.LineCollection(E, colors=['#2d5986'], linewidths=2, alpha=0.5)

        ax.add_collection(edge_collections)
        ax.set_ylim(y_min - 1, 1)
        ax.set_xlim(x_min - 1, x_max + 1)
        if title:
            ax.set_title(title)

    def insert(self, where=None, data=None, inlast=False):

        if not self.root:
            node = CTreapNode(data=data, size=1)
            self.root = node
            self.first = node
            self.last = node
            return node
        elif inlast:  # It means that this node is the new last
            node = self._insert(where=self.last, data=data)
            self.last.suc = node
            self.last = node
            self.last.suc = self.first
            self.first.pred = node
        else:
            node = self._insert(where=where, data=data)
        # UPDATE SIZE OF PARENTS
        p = node.parent
        while p:
            p.update_size()
            p = p.parent
        return node

    def _insert(self, where, data=None):
        '''
        (TODO) different balance : just from the children to the root
        Insert a node in the Treap after 'where' (a node of the CTreap)
        Idea : If where doesn't have any right children, given the fact that the current node
        come after 'where', we can add it directly, it respects the order
        Otherwise the idea is to put it just before the node that came before 'where'
        so has left children of the successor of 'where'.
        :param key:
        :param data:
        :param priority:
        :param suc:
        :param pred:
        :return:
        '''
        if not where.right:
            node = CTreapNode(data=data, size=1, parent=where, pred=where, suc=where.suc)
            where.right = node
            if where.suc:
                where.suc.pred = node
            where.suc = node
            self.balance()
            return node
        suc = where.suc
        node = CTreapNode(data=data, size=1, parent=suc, pred=where, suc=suc)
        if suc.left:
            print("Noeud left a dejà un voisin, bizarre")
            raise ValueError
        suc.left = node
        suc.pred = node
        where.suc = node
        self.balance()
        return node

    def find_root(self, node):
        '''
        Find the root of the current node
        :param node:
        :return:
        '''
        current = node
        while current.parent:
            current = current.parent
        return current

    def find_first(self):
        current = self.root
        while current.left:
            current = current.left
        return current

    def find_last(self):
        current = self.root
        while current.right:
            current = current.right
        return current

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
        :Status: OK
        :return:
        '''
        self.root = self._balance(self.root)

    def remove(self,node):
        '''
        Remove the node
        :param node: Node to remove
        :return:
        '''
        if node == self.first:
            self.first = node.suc
        if node == self.last:
            self.last = node.pred
        if node.suc:
            node.suc.pred = node.pred
        if node.pred:
            node.pred.suc = node.suc

        if node.parent.left == node:
            # print("Our node is a Left child")
            p = node.parent
            p.left = self._remove(node)
        else:
            # print("Our node is a right child")
            p = node.parent
            p.right = self._remove(node)
        # UPDATE SIZE OF PARENTS
        while p:
            p.update_size()
            p = p.parent


    def _remove(self,node):
        if not node.left and not node.right:
            return None
        elif not node.left:
            if node.parent:
                node.right.parent = node.parent
            return node.right
        elif not node.right:
            if node.parent:
                node.left.parent = node.parent
            return node.left
        else:
            if node.left.priority < node.right.priority:
                print("Right rotation")
                node = node.right_rotation()    # Rotation already deals with filiation
                node.right = self._remove(node.right)
            else:
                print("Left rotation")
                node = node.left_rotation()     # Rotation already deals with filiation
                node.left = self._remove(node.left)
        return node

    def split(self, where):
        '''
        (TODO) YA un truc à optimiser au niveau des pointeurs etc....
        :param key:
        :return:
        '''
        print(" Split on :", where.data)
        after_where = where.suc
        first = self.first
        last = self.last
        s = self.insert(where)
        s.priority = 1 * 10 ** -9
        self.balance()
        T_left = s.left
        T_right = s.right
        if T_left:
            T_left.parent = None
        if T_right:
            T_right.parent = None
        # if s.pred:  # ==WHERE
        #     s.pred.suc = first
        # if s.suc:   # == AFTER WHERE
        #     s.suc.pred = last

        T_left = CTreap(T_left)
        if T_right:
            T_right = CTreap(T_right)

        T_left.first = first
        first.pred = where
        T_left.last = where
        where.suc = first

        if T_right:
            T_right.first = after_where
            after_where.pred = last
            T_right.last = last
            last.suc = after_where

        return T_left, T_right

    def reroot(self, N):
        N.priority = 1 * (10 ** -9)
        self.balance()
        N.priority = random.random()
        # Also put in first position in euler tour
        self.first = N
        self.last = N.pred

    def releaf(self, N):
        N.priority = 1
        self.balance()
        N.priority = random.random()
        # Also put in last position in euler tour
        self.last = N
        self.first = N.suc


def union_treap(T1, T2):
    first = T1.first
    last = T2.last

    if not T2:
        return
    T1, T2 = T1.root, T2.root
    # We get the right most leaf of T1
    rl = T1
    while rl.right:
        rl = rl.right

    # We get the left most leaf of T2
    ll = T2
    while ll.left:
        ll = ll.left

    # We concat the induced euler tour
    # Maximum of first tree with minimum of second tree
    rl.suc = ll
    ll.pred = rl
    new_root = _union_treap(T1, T2)
    new_root.parent = None
    T = CTreap(new_root)
    T.first = first
    T.first.pred = last
    T.last = last
    T.last.suc = first
    return T


def _union_treap(T1, T2):
    if not T1:
        return T2
    elif not T2:
        return T1
    elif T1.priority < T2.priority:
        T1.right = _union_treap(T1.right, T2)
        T1.right.parent = T1
        T1.update_size()
        return T1
    else:
        T2.left = _union_treap(T1, T2.left)
        T2.left.parent = T2
        T2.update_size()
        return T2
