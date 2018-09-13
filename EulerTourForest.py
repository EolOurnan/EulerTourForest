from collections import defaultdict
from EulerTourTrees import EulerTourTrees
# Source  : https://dl.acm.org/citation.cfm?id=320215

# TODO :Fonction de refactor à la fin (pour les composantes temporelles à stocker)

# TODO : Utiliser des list ou des dict pour les pointers vers les données des noeuds
#      - Utiliser un dictionnaire noeud_to_pos : qui donne l'occurence du noeud dans son arbre

# TODO :? Utiliser les temps de départ des noeuds en lieu et place des priority des TreapNode ?
# MIEUX : - Lors des stream graphs : prendre le liens qui partent le plus tard comme tree edges
#        - Lorsqu'on remplace un tree edge, prendre un non tree edge qui part le plus tard possible,
#          du coup les choisir dans l'ordre de départ inverse (héhé)

# TODO: -Fonction balance des keys (utile pour edgeremoval or edgeinsertion in a ETT)
# TODO: - Fonction balance des priority (utile pour removal or insertion in a TREAP)


from EulerTourTrees import construct_euler_tour_tree


def spanning_forest_from_edge_list(edge_list):
    '''
    Construct a spanning forest from an edge list (graph may be disconnected)
    :param edge_list: [(u1,u2),(u0,u2),....]
    :return: Spanning Forest, which is a list of tuple : [(tree edge, non tree edge),...]
    '''
    a_l = defaultdict(set)
    for l in edge_list:
        u,v = l
        a_l[u].add(v)
        a_l[v].add(u)
    spanning_forest = []
    nodes = set(a_l.keys())
    while nodes:
        tree_edges = set()
        node = nodes.pop()
        visited, queue = set(),[node]
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
                    tree_edges.add((prev[node],node))
        # To get non tree edges
        non_tree_edges = set()
        for u in visited:
            for v in a_l[u]:
                if (v,u) in tree_edges or (u,v) in tree_edges:
                    continue
                elif (v,u) in non_tree_edges:
                    continue
                else:
                    non_tree_edges.add((u,v))
        nodes-=visited
        spanning_forest.append((tree_edges,non_tree_edges))
    return spanning_forest

def construct_euler_tour_forest(edge_list):
    '''
    Construct an Euler Tour Forest from an edge list (the initial graph may be disconnected)
    :param edge_list:
    :return:
    '''
    SF = spanning_forest_from_edge_list(edge_list)
    node_2_tree = {}
    Trees = []
    cnt_trees = 0

    for tree_edges,non_tree_edges in SF:
        print("Tree edges :",tree_edges)
        print("Non tree edges :",non_tree_edges)
        ETT = construct_euler_tour_tree(list(tree_edges))
        for l in tree_edges:    # Every node is present in tree edges
            node_2_tree[l[0]] = cnt_trees
            node_2_tree[l[1]] = cnt_trees
        non_tree_edges_a_l = defaultdict(set)
        for l in non_tree_edges:
            u,v= l
            non_tree_edges_a_l[u].add(v)
            non_tree_edges_a_l[v].add(u)
        ETT.nt_al = non_tree_edges_a_l
        Trees.append(ETT)
        cnt_trees += 1

    return EulerTourForest(trees=Trees,node_2_tree=node_2_tree)


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


    def search(self,e):
        if e in self.edge_2_level:
            return True #
        else:
            return False    #Rajouter un cas où les noeuds sont présents tous les deux MAIS dans des arbres différents

    def insert(self,e):
        '''
        Insert and edge in the Forest at the level 0
        :param e:
        :return:
        '''
        if not self.search(e):
            self.forests[0].insert_edge(e) # We insert the edge in the level 0
            self.edge_2_level[e] = 0

    def remove(self, e):
        '''
        REMOVE AN EDGE in the current forest
        :param e:
        :return:
        '''
        if e in self.edge_2_level:
            self.replace(e,self.edge_2_level[e])

    def replace(self,e,level):
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
            # Soit f un nontree dedges:
            #  - Si f ne connecte pas u_tree et v_tree, le move to the level i+1
            #  - Si f reconnecte u_tree and v_tree insert(f) and in u_tree

class EulerTourForest(object):
    '''
    Custom Data Structure Consisting in a Forest of Euler Tour Tree
    In the same manner as a Spanning forest if composed of Spanning Tree
    '''
    def __init__(self, trees=[], node_2_tree={}):
        '''
        # TODO: MUST FOllow node 2 tree, number 1 Piority
        :param trees:  List of trees constituting the spanning forest (each Tree an EulerTourTree)
        :param node_2_tree : List of node position in the forest : the index of the tree in :param trees:
        '''
        self.trees = trees
        self.node_2_tree = node_2_tree

    def __repr__(self):
        rp = "Node to tree : "+ str(self.node_2_tree)+"\n"
        for i in range(len(self.trees)):
            rp+=str(self.trees[i])+"\n"
        return rp

    def check_edge_presence(self,e):
        '''
        Check if the edge is in the current spanning forest
        :param e:
        :return:
        '''
        if e[0] not in self.node_2_tree:
            return False
        if e[1] not in self.node_2_tree:
            return False
        return True

    def check_edge_endpoints(self,e):
        '''
        Check if one of the endpoints is present in th forest
        :param e:
        :return:
        '''
        if e[0] in self.node_2_tree:
            return True
        if e[1] in self.node_2_tree:
            return True
        return False



    def insert_edge(self, e):
        '''
        Insert an edge in the Euler Tour Forest
        :param e:
        :return:
        '''
        u,v = e
        u_pos = self.node_2_tree[u]
        v_pos = self.node_2_tree[v]
        if u_pos == v_pos:  # They are already in the same tree
            print(" Insert in tree number :",u_pos)
            self.trees[u_pos].insert(e)
        else:  # They are in different trees
            print(" Merge Trees ",v_pos," and ",u_pos)
            u_tree = self.trees[u_pos]
            v_tree = self.trees[v_pos]
            uv_tree = EulerTourTrees.link_ett(u_tree,v_tree,e)
            # TODO : Actualize position of nodes in v_tree
            self.trees[u_pos] = uv_tree
            self.node_2_tree[v] = u_pos
            self.trees[v_pos] = None
        return



    def remove_edge(self, e):
        '''
        Remove an edge from the Euler Tour Forest
        :param e:
        :return:
        '''
        e_pos = self.node_2_tree[e[0]]
        print(" Remove in tree number :",e_pos)
        R = self.trees[e_pos].cut(e)
        # TODO : edge_2_pos to fix
        if R:
            for ETT in R:
                self.trees.append(ETT)
                l = len(self.trees)-1
                for v in self.node_2_tree:
                    if (v,v) not in ETT.tree_edge_2_pos:
                        self.node_2_tree[v] = None
                    else:
                        node_key = ETT.tree_edge_2_pos[(v,v)][0]
                        if ETT.tree.search(node_key):
                            self.node_2_tree[v] = l
            self.trees[e_pos] = None

    def reformat(self):
        # TODO : Output the connected component
        return


def dynamic_connectivity(E,M):
    ETF = construct_euler_tour_forest(E)
    print("Initial Euler Tour Forest :\n",ETF)
    while M:
        c,u,v = M.pop()
        if c == -1 : # Deletion
            print("\nDeletion : ",(u,v))
            ETF.remove_edge((u, v))
        if c == 1 : # Insertion
            print("\nInsertion : ",(u,v))
            ETF.insert_edge((u, v))
        print("ETF :\n",ETF)
        print()

    print("ETF after sequence :\n",ETF)
    G = ETF.reformat()
    return G




if __name__ == '__main__':
    # Step 1 : Get a Spanning Forest of the current graph :
    # Step 2 : Store non tree edges according to their spanning tree:

    # Step 3 : Compute the Euler Tour of each spanning tree and store it in an EulerTourTree

    # Step 4 : Compute the operations, add(link) and remove(link) on the EulerSpanningForest
    E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6),(3,4),(5,6),(2,3),
         (7, 8), (9, 7),
         #(10,11),(11,12),
         #(13,14)
         ] # Initial edge list
    # M = [(-1,0,1),(1,8,9),(-1,1,2),(-1,4,5),(1,0,1)] # Edges Insertion And Deletion
    M = [(-1, 4, 5), (-1, 4, 6)]
    # M = [(-1,1,3),(-1,1,2),(-1,4,5),(-1,4,6)]
    dynamic_connectivity(E,M)