

from collections import defaultdict
from EulerTourTrees import construct_euler_tour_tree
from EulerTourForest import construct_euler_tour_forest
from Treaps import Treap,TreapNode


if __name__ == '__main__':
    E = [(0, 1), (1, 3), (1, 2), (2, 4), (4, 5), (4, 6),(3,4)]
    Data = {0:[0,1,2,3],
            1:[0,4,5,8],
            2:[],
            3:[8,9,10,11],
            4 :[],5:[],6:[]}

