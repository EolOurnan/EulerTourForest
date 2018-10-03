Euler Tour Forest
=================

This project implements a simplified version of a fully-dynamic connectivity algorithm see :
https://dl.acm.org/citation.cfm?id=320215

Algorithm
=========
- Construct a spanning forest of the current graph. (it can be random, start with a DFS at any node)
- Store links which aren't present in the spanning forest, we call them non tree edges.
- Compute the Euler Tour of each spanning tree and store it in an Euler Tour Tree, which are built as a custom Treap
- Using these data structures we can perfom the following operations:

    - The insertion of a link may add a new tree edge, (if an isolated node is added) or a non tree edge which is easy to cope with. Otherwise the link will connect two Euler Tour Tree which can be done in $O(m∗log(n/m))$ ($m$ is the size of the smallest tree).
    - The deletion of a non tree edge doesn’t break connectivity, we can simply remove it. Otherwise the deletion of a tree edge may need a replacement that can be found in sampling non tree edge until a replacement has been found, if that can’t be done, Euler Tour Tree structure can be splitted in $O(log(n))$.
