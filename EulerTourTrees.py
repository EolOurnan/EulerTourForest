import matplotlib.pyplot as plt
from collections import defaultdict
from Chained_Treap import union_treap,CTreap


# 'TODO' ALLLL

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
    def __init__(self, tree=None, tree_edge_2_node=None,
                 nt_al = None, weight=None):
        '''

        :param tree: A Treap
        :param tree_edge_2_node: A dictionary associating a tree edge to his key
        :param nt_al: An adjacency set for non tree edges
        '''
        self.tree = tree
        self.tree_edge_2_node = tree_edge_2_node  # Edge to key in Tree
        self.nt_al = nt_al                      # Adjacency list for non tree edges (x2 already included : adj list)
        self.weight = weight                        # Sum of non tree edges adjacents to edge in tree # TODO: see self.replace()



    def __repr__(self):
        rep = " Tree edge : " + str([k for k in self.tree_edge_2_node.keys()]) + "\n"
        rep += " Non Tree edge : "+str(self.nt_al)+ "\n"
        rep += str(self.tree)
        #rep += " Euler Tour :"+str(self.get_euler_tour())+"\n"
        rep += " Priority Order :"+str(self.tree.get_data_in_priority_order())+"\n"
        return rep


    def swap_nodes(self, e1, e2):
        self.tree.swap_nodes(self.tree_edge_2_node[e1], self.tree_edge_2_node[e2])
        self.tree_edge_2_node[e2], self.tree_edge_2_node[e1] = self.tree_edge_2_node[e1], self.tree_edge_2_node[e2]


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
        return self.tree.get_euler_tour()


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
        if e in self.tree_edge_2_node:
            return True
        if (e[1],e[0]) in self.tree_edge_2_node:
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
            if e not in self.tree_edge_2_node:
                e = (e[1],e[0])
            nodes = self.tree_edge_2_node[e]
            print("  Nodes :",[i.data for i in nodes])

            # Remove the first occurence of the link :
            print("\n Remove first occurence of ",e," : ",nodes[0].data)
            J,K = self.tree.split(nodes[0])
            J.remove(nodes[0])
            J.plot(" Left after removal of "+repr(nodes[0].data))
            K.plot(" Right after removal of "+repr(nodes[0].data))
            print(" J :\n",J)
            print(" K :\n",K)
            print("\n Remove second occurence of ",e," : ",nodes[1].data)
            # Remove the second occurence of the link
            if nodes[1].data in set(K.get_euler_tour()):
                K,L = K.split(nodes[1])
                K.remove(nodes[1])
                K.plot(" Left after removal of " + repr(nodes[1].data))
                print(" K :\n", K)
                print(" L :\n", L)
                E1 = EulerTourTrees(K, self.tree_edge_2_node, self.nt_al)
                if L:
                    L.plot(" Right after removal of " + repr(nodes[1].data))
                    E2 = EulerTourTrees(union_treap(J, L), self.tree_edge_2_node, self.nt_al)
                else:
                    E2 = EulerTourTrees(J, self.tree_edge_2_node, self.nt_al)

            else:
                J,L = J.split(nodes[1])
                J.remove(nodes[1])
                J.plot(" Left after removal of " + repr(nodes[1].data))
                print(" J :\n",J)
                print(" L :\n",L)
                if K:
                    E1 = EulerTourTrees(union_treap(J,K), self.tree_edge_2_node, self.nt_al)
                else:
                    E1 = EulerTourTrees(J, self.tree_edge_2_node, self.nt_al)
                E2 = EulerTourTrees(L, self.tree_edge_2_node, self.nt_al)

            print("  E1 after cut : \n",E1)
            E1.plot("E1 after cut "+repr(e))

            print("  E2 : \n",E2)
            E2.plot("E2 after cut "+repr(e))
            del self.tree_edge_2_node[e]
            print(" # NON TREE EDGES :",self.nt_al)
            e = self.replace(E1,E2)
            if e:
                print("  Replacement edge :", e)
                print("  Found Replacement Edge :) hamdoulilah")
                E = link_ett(E1, E2, e)
                self.nt_al[e[0]].remove(e[1])
                self.nt_al[e[1]].remove(e[0])
                E.nt_al = self.nt_al
                return [E]
            else:
                print("  Did not Find Replacement Edge :( starfullah")
                return E1,E2
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
        et1 = set(E1.get_euler_tour())
        et2 = set(E2.get_euler_tour())
        for u in self.nt_al:
            if (u, u) in et1:
                for v in self.nt_al[u]:
                     if (v,v) in et2:
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
    u,v = e # We know that u is in T1 and v in T2
    u_node = T1.tree_edge_2_node[(u, u)][0]
    v_node = T2.tree_edge_2_node[(v,v)][0]
    print("   u pos :",u_node.data,"  v pos :",v_node.data)

    # RELEAF (TODO : Make a function)
    if T1.tree.last != u_node:
        L,R =T1.tree.split(where = u_node)
        T1 = EulerTourTrees(union_treap(R,L),tree_edge_2_node=T1.tree_edge_2_node)
        print("  After releafing :")
        print(T1)
        T1.plot("  T1 after releafing in :"+repr(u_node.data))

    # REROOT (TODO: Make a function)
    if T2.tree.first != v_node:
        L,R = T2.tree.split(where = v_node.pred)
        T2 = EulerTourTrees(union_treap(R,L),tree_edge_2_node=T2.tree_edge_2_node)
        print("  After rerooting :")
        print(T2)
        T2.plot("  T2 after rerooting in :"+repr(v_node.data))
    print("###########################################################")
    print("T1 first :",T1.tree.first.data)
    print("T1 last :",T1.tree.last.data)
    uv_node = T1.tree.insert(data=e,inlast=True) # (u,u) is in T1
    T1.tree_edge_2_node[e].append(uv_node)
    print("After insertion of :",e," with data :",uv_node.data)
    T1.plot("T1 after insertion of :"+repr(e))
    print(T1)
    E = union_treap(T1.tree,T2.tree)
    print(" After Union :")
    E.plot("Union of T1 and T2 ")
    print(EulerTourTrees(E,T1.tree_edge_2_node,T1.nt_al))

    vu_node = E.insert(data=(v, u),inlast=True)
    T1.tree_edge_2_node[e].append(vu_node)
    print(" After final insertion of :",(v,u)," with data :",vu_node.data)
    E = EulerTourTrees(E,T1.tree_edge_2_node)
    print(E)
    E.plot(" After Final insertion of : "+repr((v,u)))
    plt.show()
    return E


def construct_euler_tour_tree(edge_list):
    '''
    Construct an Euler Tour Tree from an edge list
    :param edge_list: An edge list
    :return: An euler tour tree
    '''
    euler_tour = euler_tour_from_edge_list(edge_list)
    T = CTreap()
    edge_2_node = defaultdict(list)
    for i,n in enumerate(euler_tour):
        node = T.insert(data=n,inlast=True)
        if (n[1],n[0]) in edge_2_node:
            edge_2_node[(n[1],n[0])].append(node)
        else:
            edge_2_node[n].append(node)
    # print("Edge occurences :",edge_2_node)
    ETT = EulerTourTrees(tree=T, tree_edge_2_node=edge_2_node)
    return ETT

