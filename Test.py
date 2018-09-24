

from collections import defaultdict
from EulerTourTrees import construct_euler_tour_tree
from EulerTourForest import construct_euler_tour_forest
from Treaps import Treap,TreapNode
import matplotlib.pyplot as plt
import random


random.seed(8)
if __name__ == '__main__':
    E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6),(3,4)]
    Data = {0:[0,1,2,3],
            1:[0,4,5,8],
            2:[],
            3:[8,9,10,11],
            4 :[],5:[],6:[]}

    ETF = construct_euler_tour_forest(E)
    ET = ETF.trees[0]
    T1 = ET.tree
    T1.plot()

    print("T1 :")
    print(ET)
    T1.reroot(4)

    T1.plot()
    print("T1 :")
    print(ET)
    plt.show()
    exit()


    print("Min value :",T1.find_min_value())
    print("Max value :", T1.find_max_value())
    key = 15
    print("Root in ",key," :")
    node = T1.search(key)
    print("Min value rooted in ",key," :",T1._find_min_value(node))
    print("Max value rooted in ",key," :",T1._find_max_value(node))
    print("Predecessor of ",key," :",T1.predecessor(node).key)
    print("Successor of ", key, " :", T1.successor(node).key)
    T1.check_invariants()

    key_1,key_2 = 7,15
    node_1,node_2 = T1.search(key_1),T1.search(key_2)
    print("Cyclic shift ",key_1," :")
    ET.cyclic_shift((4,4))
    T1.check_invariants()
    T1.plot()
    plt.show()
