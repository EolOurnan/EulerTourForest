import random
from collections import defaultdict

from EulerTourTree import construct_euler_tour_tree, union_treap


# Source  : https://dl.acm.org/citation.cfm?id=320215


# TODO :? Utiliser les temps de départ des noeuds en lieu et place des priority des TreapNode ?
#  MIEUX : - Lors des stream graphs : prendre le liens qui partent le plus tard comme tree edges
#        - Lorsqu'on remplace un tree edge, prendre un non tree edge qui part le plus tard possible,
#          du coup les choisir dans l'ordre de départ inverse (héhé)


def spanning_forest_from_edge_list(edge_list):
    '''
    Construct a spanning forest from an edge list (graph may be disconnected)
    :param edge_list: [(u1,u2),(u0,u2),....]
    :return: Spanning Forest, which is a list of tuple : [(tree edge, non tree edge),...]
    '''
    a_l = defaultdict(set)
    for l in edge_list:
        u, v = l
        a_l[u].add(v)
        a_l[v].add(u)
    spanning_forest = []
    nodes = set(a_l.keys())
    while nodes:
        tree_edges = set()
        node = nodes.pop()
        visited, queue = set(), [node]
        prev = {}
        # DFS to get spanning tree (tree edges)
        while queue:
            node = queue.pop()
            if node not in visited:
                visited.add(node)
                nodes_to_visit = a_l[node] - visited
                queue.extend(nodes_to_visit)
                for n in nodes_to_visit:
                    prev[n] = node
                if node in prev:
                    tree_edges.add((prev[node], node))
        # To get non tree edges
        non_tree_edges = set()
        for u in visited:
            for v in a_l[u]:
                if (v, u) in tree_edges or (u, v) in tree_edges:
                    continue
                elif (v, u) in non_tree_edges:
                    continue
                else:
                    non_tree_edges.add((u, v))
        nodes -= visited
        spanning_forest.append((tree_edges, non_tree_edges))
    return spanning_forest


def construct_euler_tour_forest(edge_list):
    '''
    Construct an Euler Tour Forest from an edge list (the initial graph may be disconnected)
    :param edge_list:
    :return:
    '''
    SF = spanning_forest_from_edge_list(edge_list)
    tree_edge_2_node = {}
    tree_edge_2_tree = {}
    Trees = []
    non_tree_edges_al = defaultdict(set)
    for tree_edges, non_tree_edges in SF:
        print("Tree edges :", tree_edges)
        print("Non tree edges :", non_tree_edges)
        ETT, d = construct_euler_tour_tree(list(tree_edges))
        tree_edge_2_node.update(d)
        for l in tree_edges:  # Every node is present in tree edges
            if l[0] not in tree_edge_2_tree:
                tree_edge_2_tree[l[0]] = ETT
            if l[1] not in tree_edge_2_tree:
                tree_edge_2_tree[l[1]] = ETT
        for l in non_tree_edges:
            u, v = l
            non_tree_edges_al[u].add(v)
            non_tree_edges_al[v].add(u)
        Trees.append(ETT)
    return EulerTourForest(trees=Trees, tree_edge_2_tree=tree_edge_2_tree, tree_edge_2_node=tree_edge_2_node,
                           non_tree_edges_al=non_tree_edges_al)


class ETF_collections(object):
    '''
    Collection of Spanning Euler Forest (1 for each level of the algorithm)
    '''

    def __init__(self):
        '''
        Forests : A list of Spanning Forests of different levels
        Edge_2_level : A dictionary associating an edge to his current level
        '''
        self.forests = []
        self.edge_2_level = {}

    def search(self, e):
        if e in self.edge_2_level:
            return True  #
        else:
            return False  # Rajouter un cas où les noeuds sont présents tous les deux MAIS dans des arbres différents

    def insert(self, e):
        '''
        Insert and edge in the Forest at the level 0
        :param e:
        :return:
        '''
        if not self.search(e):
            self.forests[0].insert_edge(e)  # We insert the edge in the level 0
            self.edge_2_level[e] = 0

    def remove(self, e):
        '''
        REMOVE AN EDGE in the current forest
        :param e:
        :return:
        '''
        if e in self.edge_2_level:
            self.replace(e, self.edge_2_level[e])

    def replace(self, e, level):
        '''
        REPLACE A TREE EDGE
        :param e: edge
        :param level: level of the edge to replace in the forest
        :return:
        '''
        while level > 0:
            status = self.forests[level].replace(e)
            if status:
                return
            level -= 1
            # return No replacement found, du coup ya du split dans l'air, done with .remove(e) ???
            # Move all edges of v_tree to the level i+1
            # Récuperer les non tree edges de v_tree et tester si il y en a qui reconnecte u_tree et v_tree
            #  Soit f un nontree dedges:
            #  - Si f ne connecte pas u_tree et v_tree, le move to the level i+1
            #  - Si f reconnecte u_tree and v_tree insert(f) and in u_tree


class EulerTourForest(object):
    '''
    Custom Data Structure Consisting in a Forest of Euler Tour Tree
    In the same manner as a Spanning forest if composed of Spanning Tree
    '''

    def __init__(self, trees=[], tree_edge_2_tree={}, tree_edge_2_node={}, non_tree_edges_al=defaultdict(set)):
        '''
        :param trees:  List of trees constituting the spanning forest (each Tree an EulerTourTree).
        :param tree_edge_2_tree: Dictionary associating a tree edge -> Euler Tour Tree it belongs
        :param tree_edge_2_node : Dictionary associating a tree edge -> the corresponding node (CTreapNode)
        :param non_tree_edges_al: Adjacency List (set) of non tree edges.
        '''
        self.trees = trees
        self.tree_edge_2_tree = tree_edge_2_tree
        self.tree_edge_2_node = tree_edge_2_node
        self.non_tree_edges_al = non_tree_edges_al

    def __repr__(self):
        rep = " Tree edges : " + str([k for k in self.tree_edge_2_node.keys()]) + "\n"
        rep += "Tree edges to tree :" + str([(n, v.root.data) for n, v in self.tree_edge_2_tree.items()]) + "\n"
        rep += " Non Tree edges : " + str(self.non_tree_edges_al) + "\n"
        for i in range(len(self.trees)):
            rep += str(self.trees[i]) + "\n"
        return rep

    def is_tree_edge(self, e):
        '''
        Return true if *e* is tree edge, false otherwise
        :param e: an edge
        :return:
        '''
        if e in self.tree_edge_2_node:
            return e
        if (e[1], e[0]) in self.tree_edge_2_node:
            return (e[1], e[0])
        return False

    def plot(self, title=None):
        '''
        Plot the Euler Tour Trees in the Euler Tour Forest
        :param title: An optional title
        :return:
        '''
        for i, T in enumerate(self.trees):
            if title:
                T.plot(title)
            else:
                T.plot(str(i) + " Tree of the Euler Tour Forest ")

    def check_edge_presence(self, e):
        '''
        Check if the edge is in the current spanning forest
        :param e:
        :return:
        '''
        if e[0] not in self.tree_edge_2_node:
            return False
        if e[1] not in self.tree_edge_2_node:
            return False
        return True

    def check_edge_endpoints(self, e):
        '''
        Check if one of the endpoints is present in th forest
        :param e:
        :return:
        '''
        if e[0] in self.tree_edge_2_node:
            return True
        if e[1] in self.tree_edge_2_node:
            return True
        return False

    def insert_edge(self, e):
        '''
        Insert an edge in the Euler Tour Forest
        :param e:
        :return:
        '''

        def insert(self, e):
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

        u, v = e
        u_tree_number = self.tree_edge_2_node[u]
        v_tree_number = self.tree_edge_2_node[v]
        if u_tree_number == v_tree_number:  # They are already in the same tree
            print(" Insert in tree number :", u_tree_number)
            self.trees[u_tree_number].insert(e)
        else:  # They are in different trees
            print(" Merge Trees ", v_tree_number, " and ", u_tree_number)
            u_tree = self.trees[u_tree_number]
            v_tree = self.trees[v_tree_number]
            uv_tree = self.link_ett(u_tree, v_tree, e)
            # TODO : Actualize position of nodes in v_tree
            self.trees[u_tree_number] = uv_tree
            for n in v_tree.get_euler_tour():
                if n[0] == n[1]:
                    self.tree_edge_2_node[n[0]] = u_tree_number
            self.trees[v_tree_number] = None
        return

    def replace_edge(self, E1, E2):
        '''
        Find is there is a non tree edge linking E1 and E2
        :param E1: An euler tour tree
        :param E2: An euler tour tree
        :return: a replacement edge if found, false otherwise
        '''

        # We assume that E1 is smaller than E2 (TODO : implement a size of the tree (aka len(E1.nt_a_l))?
        def replacement_edge(E1, E2):
            r1 = E1.root
            r2 = E2.root
            for u in self.non_tree_edges_al:
                if self.tree_edge_2_node[(u, u)][0].find_root() == r1:
                    for v in self.non_tree_edges_al[u]:
                        if self.tree_edge_2_node[(v, v)][0].find_root() == r2:
                            return (u, v)
            return False

        e = replacement_edge(E1, E2)
        if e:
            print("  Replacement edge :", e)
            print("  Found Replacement Edge :) hamdoulilah")
            E = self.link_euler_tour_trees(E1, E2, e)
            self.tree_edge_2_tree[e[0]] = E
            self.tree_edge_2_tree[e[1]] = E
            self.non_tree_edges_al[e[0]].remove(e[1])
            self.non_tree_edges_al[e[1]].remove(e[0])
            return [E]
        else:
            print("  Did not Find Replacement Edge :( starfullah")
        return False

    def remove_edge(self, e):
        '''
        Remove an edge from the Euler Tour Forest
        :param e:
        :return:
        '''
        current_tree = self.tree_edge_2_tree[e[0]]
        print("Current TREE :\n",current_tree)
        print(" Remove in tree rooted at : ", current_tree.root.data)
        e = self.is_tree_edge(e)
        if e:
            nodes = self.tree_edge_2_node[e]
            # Cut the euler tour into two distincts euler tour corresponding
            # to the removal of *e*
            E1, E2 = current_tree.cut(nodes)
            # Try to find a replacement edge among the non tree edges
            R = self.replace_edge(E1, E2)
            if R:
                for ETT in R:
                    print(" Remove tree edge : ", e)
                    self.trees.append(ETT)
                    # for v in self.tree_edge_2_node:
                    #     if (v, v) not in self.tree_edge_2_node:
                    #         self.tree_edge_2_node[(v,v)] = None
                    #     else:
                    #         # et = set(ETT.get_euler_tour())
                    #         # if (v,v) in et:
                    #         if ETT.tree_edge_2_node[(v,v)][0].find_root() == ETT.tree.root:
                    #             self.tree_edge_2_node[v] = l
                    # TODO: tree_edge_2_tree
                del current_tree
            else:
                self.trees += [E1, E2]
            del self.tree_edge_2_node[e]
        else:
            print(" Remove non tree edge : ", e)
            u, v = e
            self.non_tree_edges_al[u].remove(v)
            self.non_tree_edges_al[v].remove(u)

    def link_euler_tour_trees(self, E1, E2, e):
        '''
        Merge two euler tour tree
        :param E1: An euler tour tree
        :param E2: An euler tour tree
        :param e: An edge
        :return:
        '''
        u, v = e  # We know that u is in E1 and v in E2
        u_node = self.tree_edge_2_node[(u, u)][0]
        v_node = self.tree_edge_2_node[(v, v)][0]
        print("   u pos :", u_node.data, "  v pos :", v_node.data)
        # Releaf
        if E1.last != u_node:
            E1 = E1.releaf(where=u_node)
            print("  After releafing :")
            print(E1)
            E1.plot("  E1 after releafing in :" + repr(u_node.data))
        # Reroot (so releaf in v_node.pred)

        if E2.first != v_node:
            E2 = E2.releaf(where=v_node.pred)
            print("  After rerooting :")
            print(E2)
            E2.plot("  E2 after rerooting in :" + repr(v_node.data))

        print("###########################################################")
        print("E1 first :", E1.first.data)
        print("E1 last :", E1.last.data)
        uv_node = E1.insert(data=e, inlast=True)  # (u,u) is in E1

        print("After insertion of :", e, " with data :", uv_node.data)
        E1.plot("E1 after insertion of :" + repr(e))
        print(E1)
        E = union_treap(E1, E2)
        print(" After Union :")
        E.plot("Union of E1 and E2 ")
        print(E)
        vu_node = E.insert(data=(v, u), inlast=True)  # (v,v) is in E2

        self.tree_edge_2_node[e] = [uv_node]
        self.tree_edge_2_node[e].append(vu_node)
        print(" After final insertion of :", (v, u), " with data :", vu_node.data)
        E.plot(" After Final insertion of : " + repr((v, u)))
        print(E)
        return E

    def reformat(self):
        #  TODO : Output the connected component
        return


import matplotlib.pyplot as plt


def dynamic_connectivity(E, M):
    ETF = construct_euler_tour_forest(E)
    print("Initial Euler Tour Forest :\n", ETF)
    ETF.plot("Initial ETT")
    while M:
        c, u, v = M.pop()
        if c == -1:  # Deletion
            print("\nDeletion : ", (u, v))
            ETF.remove_edge((u, v))
            # plt.show()
        if c == 1:  # Insertion
            print("\nInsertion : ", (u, v))
            ETF.insert_edge((u, v))
            plt.show()
        print("ETF :\n", ETF)
    print("ETF after sequence :\n", ETF)
    G = ETF.reformat()
    return G


if __name__ == '__main__':
    # Step 1 : Get a Spanning Forest of the current graph :
    # Step 2 : Store non tree edges according to their spanning tree:

    # Step 3 : Compute the Euler Tour of each spanning tree and store it in an EulerTourTree

    # Step 4 : Compute the operations, add(link) and remove(link) on the EulerSpanningForest
    random.seed(1)
    E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6), (3, 4), (5, 6), (2, 3),
         (7, 8), (9, 7),
         # (10,11),(11,12),
         # (13,14)
         ]  # Initial edge list
    # M = [(-1,0,1),(1,8,9),(-1,1,2),(-1,4,5),(1,0,1)] # Edges Insertion And Deletion
    # M = [(-1, 4, 5), (-1, 4, 6)]
    M = [(1, 4, 5), (1, 1, 2), (-1, 1, 2), (-1, 1, 3), (-1, 4, 5), (-1, 4, 6)]
    dynamic_connectivity(E, M)
