
import matplotlib.pyplot as plt
from collections import defaultdict
from Treaps import union_treaps,Treap


def euler_tour_from_edge_list(edge_list):
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
    # TODO : Rajouter un attribut size ainsi qu'un attribut weight (number of non tree edges)*2
    #  A rajouter en list, ou dict, à part
    def __init__(self, tree=None, tree_edge_2_pos=None,
                 nt_al = None):
        '''

        :param tree: A Treap
        :param tree_edge_2_pos: A dictionary associating a tree edge to his key
        :param nt_al: An adjacency set for non tree edges
        '''
        self.tree = tree
        self.tree_edge_2_pos = tree_edge_2_pos # Edge to key in Tree
        self.nt_al = nt_al #Adjacency list for non tree edges

    def __repr__(self):
        rep = "Tree edge : "+str(self.tree_edge_2_pos)+"\n"
        rep += "Non Tree edge : "+str(self.nt_al)+ "\n"
        rep += str(self.tree)
        rep += " Euler Tour :"+str(self.tree.get_data_in_key_order())+"\n"

        return rep

    def is_tree_edge(self,e):
        if e in self.tree_edge_2_pos:
            return True
        if (e[1],e[0]) in self.tree_edge_2_pos:
            return True
        return False

    def insert(self,e):
        if self.is_tree_edge(e):
            return  # Nothing to do be do be do
        # Else insert in non tree edges
        self.nt_al[e[0]].add(e[1])
        self.nt_al[e[1]].add(e[0])

    def cut(self,e):
        '''
        Remove and edge from the Euler Tour Tree
        :param e:
        :return:
        '''
        if self.is_tree_edge(e):
            print("  Tree Edge Deletion")
            if e not in self.tree_edge_2_pos:
                e = (e[1],e[0])
            positions = self.tree_edge_2_pos[e]
            print("  Positions :",positions)
            J,K = self.tree.split_on_key(positions[0])
            if J.search(positions[0]):
                J.remove(positions[0])
            if K.search(positions[1]):
                K,L = K.split_on_key(positions[1])
                K.remove(positions[1])
            E1 = EulerTourTrees(K,self.tree_edge_2_pos,self.nt_al)
            E2 = EulerTourTrees(union_treaps(J,L),self.tree_edge_2_pos,self.nt_al)
            print("  E1 : \n",E1)
            print("  E2 : \n",E2)
            del self.tree_edge_2_pos[e]
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
                return EulerTourTrees(E1, self.tree_edge_2_pos,self.nt_al),\
                       EulerTourTrees(E2, self.tree_edge_2_pos,self.nt_al)
        else:
            print("  Non Tree Edge Deletion :")
            self.nt_al[e[0]].remove(e[1])
            self.nt_al[e[1]].remove(e[0])
            return False

    def replace(self,E1,E2):
        '''
        Find is there is a non tree edge linking E1 and E2
        :param E1:
        :param E2:
        :return:
        '''
        # We assume that E1 is smaller than E2 (TODO : implement a size of the tree (aka len(E1.nt_a_l))?
        for u in self.nt_al:
            if E1.tree.search(self.tree_edge_2_pos[(u,u)][0]):
                for v in self.nt_al[u]:
                    if E2.tree.search(self.tree_edge_2_pos[(v,v)][0]):
                        return (u,v)
        return False

def link_ett(T1,T2,e):
    u,v = e
    u_pos = T1.tree_edge_2_pos[(u, u)][0]
    v_pos = T2.tree_edge_2_pos[(v,v)][0]
    print("   u pos :",u_pos,"  v pos :",v_pos)
    if T2.tree.search(u_pos):
        T1,T2 =T2,T1
    T1.tree.releaf(u_pos)
    print("After releafing :")
    print(T1)
    T2.tree.reroot(v_pos)
    print("Adter rerooting :")
    print(T2)
    key = T1.tree.get_max_value()+1
    T1.tree.insert(key=key, data=e) # Puisque l'on a rerooter T1 en u
    T1.tree_edge_2_pos[e].append(key)
    print("After insertion of :",e," with key :",key)
    print(T1)

    E = union_treaps(T1.tree,T2.tree)
    print(" After Union :")
    print(EulerTourTrees(E,T1.tree_edge_2_pos,T1.nt_al))
    key = E.get_max_value()+1
    E.insert(key= key, data=(v, u))
    T1.tree_edge_2_pos[e].append(key)
    print(" After final insertion of :",(v,u)," with key :",key)
    print(EulerTourTrees(E,T1.tree_edge_2_pos,T1.nt_al))
    return EulerTourTrees(E,T1.tree_edge_2_pos,T1.nt_al)


def construct_euler_tour_tree(edge_list):
    '''
    Construct an Euler Tour Tree from an edge list
    :param edge_list:
    :return:
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
    return EulerTourTrees(tree=T,tree_edge_2_pos=edge_2_occurences)


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