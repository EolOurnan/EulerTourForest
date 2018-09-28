


from EulerTourForest import construct_euler_tour_forest
from EulerTourTrees import EulerTourTrees
from Chained_Treap import CTreap,union_treap
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
    print("T1",ET)
    print("T1 first :",T1.first.data)
    print("T1 second :",T1.first.suc.data)
    print("T1 last :",T1.last.data)
    ############### TEST INSERTION #################
    # T1.insert(data=(5,2),where = T1.first)
    # T1.plot()
    # plt.show()
    ################################################
    ############## TEST FIND ROOT ##################
    # print("T1 root :",T1.first.find_root().data)
    # print("T1 root :",T1.last.find_root().data)
    # print("T1 root :",T1.last.pred.find_root().data)
    ################################################
    ############# TEST ROTATION ####################
    # rotate_in = T1.first.suc.suc
    # print("Rotate in :",rotate_in.data)
    # rotate_in.left_rotation()
    # print("Rotate in right :",rotate_in.right)
    # T1.plot('after left rotation in :'+repr(rotate_in.data))
    # T1.first.suc.right_rotation()
    # T1.plot('after right rotation in :'+repr(T1.first.suc.suc.data)
    ################################################
    ############# TEST DELETION ####################
    # to_remove = T1.last.pred.pred.pred.pred
    # print("Remove :",to_remove.data)
    # T1.remove(to_remove)
    # print("T1",T1)
    # T1.plot("After remove "+repr(to_remove.data))
    # plt.show()
    ################################################
    ############# TEST SPLIT  ######################
    to_split = T1.first.suc.suc.suc.suc.suc.suc.suc
    L,R =T1.split(to_split)
    # L,R = EulerTourTrees(CTreap(L)),EulerTourTrees(CTreap(R))
    L.plot("Left tree after split in "+repr(to_split.data))
    R.plot("Right tree after split in "+repr(to_split.data))
    print()
    print(" L before first :",L.first.pred.data)
    print(" L first :",L.first.data)
    print(" L last :",L.last.data)
    print(" L after last :",L.last.suc.data)
    print()
    print(" R before first :",R.first.pred.data)
    print(" R first :",R.first.data)
    print(" R last :",R.last.data)
    print(" R after last :",R.last.suc.data)
    print()

    print("L :\n",EulerTourTrees(L))
    print("R :\n",EulerTourTrees(R))
    ################################################
    ############# TEST UNION  ######################
    # E = CTreap(union_treap(L,R))
    E = union_treap(R,L)
    print(" E before first :",E.first.pred.data)
    print(" E first :",E.first.data)
    print(" E last :",E.last.data)
    print(" E after last :",E.last.suc.data)
    print("E :\n",EulerTourTrees(E))
    E.plot("Union of previous left and right ")
    plt.show()

    exit()
    print("T1 :")
    print(ET)
    key= 4
    n = T1.search(key)
    print("T1 sub pred of :",key)
    pred = T1.sub_pred(n)
    if pred:
        print(pred.key)
    else:
        print("No pred")
    print("T1 sub suc of :",key)
    suc = T1.sub_suc(n)
    if suc:
        print(suc.key)
    else:
        print("No suc")
    T1.reroot(4)

    n = T1.search(key)
    print("T1 sub pred of :",key)
    pred = T1.sub_pred(n)
    if pred:
        print(pred.key)
    else:
        print("No pred")
    print("T1 sub suc of :",key)
    suc = T1.sub_suc(n)
    if suc:
        print(suc.key)
    else:
        print("No suc")

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
