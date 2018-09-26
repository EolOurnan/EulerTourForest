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

    def left_rotation(self):
        '''
        (TODO) CHANGE SIZE ATTRIBUTE
        Perform a left rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't chang ethe cyclic order, successor and predecessor unchanged
        :return:
        '''
        root = self
        pivot = root.right

        # Change filiation
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
        (TODO) CHANGE SIZE ATTRIBUTE
        Perform a right rotation on the Treap with the current TreapNode as the root
        https://en.wikipedia.org/wiki/Tree_rotation
        Note : This doesn't chang ethe cyclic order, successor and predecessor unchanged
        :return:
        '''
        root = self
        pivot = root.left

        # Change filiation
        pivot.parent = root.parent
        root.parent = pivot
        if pivot.right:
            pivot.right.parent = root

        # Rotate
        root.left = pivot.right

        root.update_size()
        pivot.right = root

        pivot.update_size()
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

    def __repr__(self):
        return str(self.root)

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
        N.append(((x_parent, y_parent), (node.data)))  # ,node.priority))) # priority
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
            label = str(data)  # + "\n" + str(data[1])  # +"\n"+str(data[2])  #priority
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

    def insert(self, where=None, data=None, inlast=False, infirst=False):

        if not self.root:
            node = CTreapNode(data=data, size=1, parent=None, pred=None, suc=None)
            self.root = node
            self.first = node
            self.last = node
        elif inlast:  # It means that this node is the new last
            node = self._insert(where=self.last, data=data)
            self.last.suc = node
            self.last = node
            self.last.suc = self.first
            self.first.pred = node
        elif infirst:
            node = self._insert(where=self.first, data=data)
            self.first.pred = node
            self.first = node
            self.first.pred = self.last
            self.last.suc = node
        else:
            self._insert(where=where, data=data)

    def _insert(self, where, data=None):
        '''
        (TODO) different balance : just from the children to the root
        Insert a node in the Treap after 'where' (a node of the CTreap)
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
        next = where.suc
        node = CTreapNode(data=data, size=1, parent=next, pred=next, suc=where)
        next.left = node
        next.pred = node
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
        Remove the node corresponding to the key
        :param key: The key to remove
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
        removed = False
        while not removed:
            if node.left and node.right:
                if node.left.priority < node.right.priority:
                    node.right_rotation()
                    self.plot("right rotation in "+repr(node.data))
                    plt.show()
                else:
                    node.left_rotation()
                    self.plot("left rotation in "+repr(node.data))
                    plt.show()


            elif not node.left and not node.right:
                if node.parent.left ==node:
                    node.parent.left = None
                else:
                    node.parent.right = None
                removed = True
            elif not node.left:
                if node.parent.left ==node:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
                removed = True
            elif not node.right:
                if node.parent.left ==node:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
                removed = True
        # UPDATE SIZE OF PARENTS
        p = node.parent
        while p:
            p.update_size()
            p = p.parent
        node.parent = node.left = node.right = node.prev = node.next = None

        # if node.left and node.right:
        #     # The next node has no right or no left child
        #     next = node.suc
        #     self.swap_nodes(next, node)
        # if node.suc:
        #     node.suc.pred = node.pred
        # if node.pred:
        #     node.pred.suc = node.suc
        #
        # rep = None
        # if node.left:
        #     rep = node.left
        # else:
        #     rep = node.right
        # if rep:
        #     rep.parent = node.parent
        # if node.parent:
        #     if node.parent.left == node:  # If left child
        #         node.parent.left = rep
        #     else:                         # Right child
        #         node.parent.right = rep
        # # UPDATE SIZE OF PARENTS
        # p = node.parent
        # while p:
        #     p.update_size()
        #     p = p.parent
        # # Remove references to the node


    def split(self, where):
        '''
        (TODO) YA un truc à optimiser au niveau des pointeurs etc....
        :param key:
        :return:
        '''
        print(" Split on :", where.data)
        s = self.insert(where)
        s.priority = 1 * 10 ** -9
        self.balance()
        T_left = s.left
        T_right = s.right
        if T_left:
            T_left.parent = None
        if T_right:
            T_right.parent = None
        if s.pred:
            s.pred.suc = None
        if s.suc:
            s.suc.pred = None
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
        ll = ll.right

    # We concat the induced euler tour
    # Maximum of first tree with minimum of second tree
    rl.suc = ll
    ll.pred = rl
    new_root = _union_treap(T1, T2)
    new_root.parent = None
    return new_root


def _union_treap(T1, T2):
    if not T1:
        return T2
    elif not T2:
        return T1
    elif T1.priority < T2.priority:
        T1.right = union_treap(T1.right, T2)
        T1.right.parent = T1
        T1.update_size()
        return T1
    else:
        T2.left = union_treap(T1, T2.left)
        T2.left.parent = T2
        T2.update()
        return T2
