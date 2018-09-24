
import matplotlib.pyplot as plt
from collections import defaultdict
from Treaps import union_treaps,Treap


def euler_tour_from_edge_list(edge_list):
    '''
    Compute the euler tour of a graph ( with edges, including self loops,
     instead of nodes)
    :param edge_list: An edge list
    :return: A lsit containing the euler tour
    '''
    a_l = defaultdict(list)
    for l in edge_list:  # Create edge list (2*m links)
        u, v = l
        a_l[u].append(v)
        a_l[v].append(u)
    tour = []
    current_node = edge_list[0][0]
    queue = [current_node]
    while queue:
        if a_l[current_node]:
            queue.append(current_node)
            current_node = a_l[current_node].pop()
        else:
            tour.append(current_node)
            current_node = queue.pop()
    edge_tour = []
    seen = set()
    for i in range(len(tour)-1):
        u = tour[i]
        if u not in seen:
            seen.add(u)
            edge_tour.append((u,u))
        edge_tour.append((u,tour[i+1]))
    return edge_tour

def plot_euler_tour_tree(root,pos = None):
    if not pos:
        pos = [0,0]
    else:
        plt.plot([pos[0]],[pos[1]],'ok')
        plt.annotate((str(root.key)+"|"+str(root.data)+"|"+str(root.priority)),
                     xy = pos, xycoords='data')
    if not root.right and not root.left:
        return
    if root.right:
        pos = [pos[0]+1,pos[1]-1]
        plot_euler_tour_tree(root.right,pos)
    if root.left:
        pos = [pos[0]-1,pos[1]-1]
        plot_euler_tour_tree(root.left,pos)



class EulerTourTrees(object):
    #  A rajouter en list, ou dict, à part
    def __init__(self, tree=None, tree_edge_2_keys=None,
                 nt_al = None, size=None):
        '''

        :param tree: A Treap
        :param tree_edge_2_keys: A dictionary associating a tree edge to his key
        :param nt_al: An adjacency set for non tree edges
        '''
        self.tree = tree
        self.tree_edge_2_keys = tree_edge_2_keys  # Edge to key in Tree
        self.nt_al = nt_al                      # Adjacency list for non tree edges (x2 already included : adj list)
        self.size = size                        # Sum of non tree edges adjacents to edge in tree # TODO: see self.replace()



    def __repr__(self):
        rep = "Tree edge : " + str(self.tree_edge_2_keys) + "\n"
        rep += " Non Tree edge : "+str(self.nt_al)+ "\n"
        rep += str(self.tree)
        rep += " Euler Tour :"+str(self.get_euler_tour())+"\n"
        rep += " In order :"+str(self.tree.get_data_in_key_order())+"\n"
        rep += " Priority Order :"+str(self.tree.get_data_in_priority_order())+"\n"

        return rep

    def find_min_value(self):
        return self.tree.find_min_value()

    def find_max_value(self):
        return self.tree.find_max_value()

    def swap_nodes(self, e1, e2):
        self.tree.swap_nodes(self.tree_edge_2_keys[e1], self.tree_edge_2_keys[e2])
        self.tree_edge_2_keys[e2], self.tree_edge_2_keys[e1] = self.tree_edge_2_keys[e1], self.tree_edge_2_keys[e2]


    def get_in_order(self):
        '''
        Return the in-order representation of the Tree
        :return:
        '''
        in_order = self.tree.get_data_in_key_order()
        return in_order

    def get_euler_tour(self):
        '''
        Return the induced euler tour representation of the Tree
        :return:
        '''
        euler_tour = [self.tree.first.data]
        current = self.tree.first.suc
        while current != self.tree.first:
            euler_tour.append(current.data)
            current = current.suc
        return euler_tour


    def plot(self,title=None):
        '''
        Plot the euler Tour tree
        :param title:
        :return:
        '''
        self.tree.plot(title)

    def is_tree_edge(self,e):
        '''
        Return true if :param e: is tree edge, false otherwise
        :param e: an edge
        :return:
        '''
        if e in self.tree_edge_2_keys:
            return True
        if (e[1],e[0]) in self.tree_edge_2_keys:
            return True
        return False

    def insert(self,e):
        '''
        Insert an edge into the euler tour tree
        :param e: an edge
        :return:
        '''
        if self.is_tree_edge(e):
            return  # Nothing to do be do be do
        # Else insert in non tree edges, same cost as checking if its already a non tree edge
        self.nt_al[e[0]].add(e[1])
        self.nt_al[e[1]].add(e[0])

    def cut(self,e):
        '''
        Remove and edge from the Euler Tour Tree
        :param e: an edge
        :return:
        '''
        if self.is_tree_edge(e):
            print("  Tree Edge Deletion")
            if e not in self.tree_edge_2_keys:
                e = (e[1],e[0])
            positions = self.tree_edge_2_keys[e]
            print("  Positions :",positions)
            J,K = self.tree.split_on_key(positions[0])
            if J.search(positions[0]): # USELESS TEST
                J.remove(positions[0])
            if K.search(positions[1]): # USELESS TEST
                K,L = K.split_on_key(positions[1])
                K.remove(positions[1])
            E1 = EulerTourTrees(K, self.tree_edge_2_keys, self.nt_al)
            print("  E1 : \n",E1)
            E1.plot("E1 after cut "+repr(e))

            E2 = EulerTourTrees(union_treaps(J,L), self.tree_edge_2_keys, self.nt_al)
            print("  E2 : \n",E2)
            E2.plot("E2 after cut "+repr(e))
            del self.tree_edge_2_keys[e]
            e = self.replace(E1,E2)
            if e:
                E = link_ett(E1, E2, e)
                print("  Replacement edge :", e)
                print("  Found Replacement Edge :) hamdoulilah")
                E.nt_al[e[0]].remove(e[1])
                E.nt_al[e[1]].remove(e[0])
                return [E]
            else:
                print("  Did not Find Replacement Edge :( starfullah")
                return EulerTourTrees(E1, self.tree_edge_2_keys, self.nt_al),\
                       EulerTourTrees(E2, self.tree_edge_2_keys, self.nt_al)
        else:
            print("  Non Tree Edge Deletion :")
            self.nt_al[e[0]].remove(e[1])
            self.nt_al[e[1]].remove(e[0])
            return False

    def replace(self,E1,E2):
        '''
        Find is there is a non tree edge linking E1 and E2
        :param E1: An euler tour tree
        :param E2: An euler tour tree
        :return: a replacement edge if found, false otherwise
        '''
        # We assume that E1 is smaller than E2 (TODO : implement a size of the tree (aka len(E1.nt_a_l))?
        for u in self.nt_al:
            if E1.tree.search(self.tree_edge_2_keys[(u, u)][0]):
                for v in self.nt_al[u]:
                    if E2.tree.search(self.tree_edge_2_keys[(v, v)][0]):
                        return (u,v)
        return False

def link_ett(T1,T2,e):
    '''
    Merge two euler tour tree
    :param T1: An euler tour tree
    :param T2: An euler tour tree
    :param e: An edge
    :return:
    '''
    u,v = e
    u_pos = T1.tree_edge_2_keys[(u, u)][0]
    v_pos = T2.tree_edge_2_keys[(v,v)][0]
    print("   u pos :",u_pos,"  v pos :",v_pos)
    if T2.tree.search(u_pos):
        T1,T2 =T2,T1
    T1.tree.releaf(u_pos)
    print("After releafing :")
    T1.plot("T1 after releafing in :"+repr(u_pos))
    print(T1)
    T2.tree.reroot(v_pos)
    print("Adter rerooting :")
    T2.plot("T2 after rerooting in :"+repr(v_pos))
    print(T2)
    key = T1.tree.find_max_value() + 1
    T1.tree.insert(key=key, data=e) # Puisque l'on a rerooter T1 en u
    T1.tree_edge_2_keys[e].append(key)
    print("After insertion of :",e," with key :",key)
    T1.plot("T1 after insertion of :"+repr(e)+" with key :"+repr(key))
    print(T1)
    E = union_treaps(T1.tree,T2.tree)
    print(" After Union :")
    E.plot("Union of T1 and T2 ")
    print(EulerTourTrees(E,T1.tree_edge_2_keys,T1.nt_al))
    key = E.find_max_value() + 1
    E.insert(key= key, data=(v, u))
    T1.tree_edge_2_keys[e].append(key)
    print(" After final insertion of :",(v,u)," with key :",key)
    E = EulerTourTrees(E,T1.tree_edge_2_keys,T1.nt_al)
    print(E)
    E.plot(" After Final insertion of : "+repr((v,u))+" with key :"+repr(key))
    return E


def construct_euler_tour_tree(edge_list):
    '''
    Construct an Euler Tour Tree from an edge list
    :param edge_list: An edge list
    :return: An euler tour tree
    '''
    euler_tour = euler_tour_from_edge_list(edge_list)
    T = Treap()
    edge_2_occurences = defaultdict(list)
    for i,n in enumerate(euler_tour):
        if (n[1],n[0]) in edge_2_occurences:
            edge_2_occurences[(n[1],n[0])].append(i)
        else:
            edge_2_occurences[n].append(i)
        T.insert(key=i,data=n)
    print("Edge occurences :",edge_2_occurences)
    return EulerTourTrees(tree=T, tree_edge_2_keys=edge_2_occurences)


#
# if __name__ == '__main__':
#     E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6),(3,4)]
#     Data = {0:[0,1,2,3],
#             1:[0,4,5,8],
#             2:[],
#             3:[8,9,10,11],
#             4 :[],5:[],6:[]}
#
#     euler_tour = euler_tour_from_edge_list(E)
#     print("Euler tour :\n", euler_tour)
#     ETT = Treap()
#     edge_2_occurences = defaultdict(list)
#     for i,n in enumerate(euler_tour):
#         if (n[1],n[0]) in edge_2_occurences:
#             edge_2_occurences[(n[1],n[0])].append(i)
#         else:
#             edge_2_occurences[n].append(i)
#         ETT.insert(key=i,data=n)
#     print("Edge 2 occurences :",edge_2_occurences)
#     ETT = EulerTourTrees(ETT,edge_2_occurences)
#     print("ETT :\n",ETT)
#     print(ETT.tree.get_data_in_key_order())
#     e = (1,2)
#     E1,E2 = ETT.cut(e)
#     print("E1 :", E1)
#     print(E1.tree.get_data_in_key_order())
#     print()
#     print("E2 :", E2)
#     print(E2.tree.get_data_in_key_order())
#     ETT = link_ett(E1,E2,e)
#     ETT.tree.balance()
#     print(" after link ETT :\n", ETT)
#     print("KEY :")
#     print(ETT.tree.get_data_in_key_order())