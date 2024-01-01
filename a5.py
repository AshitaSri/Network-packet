#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ashita
"""



class MaxHeap:
    '''
    will be used in the Dijkastra Algorithm (slightly modified)
    follows 0 base indexing 
    '''
    def __init__(self):
        self._arr = []
        return 
    def empty(self):
        return len(self._arr) == 0
    def put(self, x):
        i = len(self._arr)
        self._arr.append(x)
        self.heapup(i)
        return 
    def get(self):
        ans = self._arr[0]
        if len(self._arr) > 1:
            self._arr[0] = self._arr.pop()
        elif len(self._arr) == 1:
            self._arr = [] 
        self.heapdown(0)
        return ans
    def heapup(self, i):
        curr = i;
        while (curr >0):
            parent_i =(curr-1)//2   
            if (self._arr[parent_i] < self._arr[curr]):
                self.swap(curr, parent_i)
                curr = parent_i
            else:
                break
        return 
    def heapdown(self, i):
        l = self._arr
        parent = i
        while (parent <= (len(l)-1)):
            b = True
            if parent*2 + 2 < len(l):
                rightChild = l[parent*2 + 2]
            else :
                rightChild = (-1, -1)
            if parent*2 + 1 < len(l):
                b = False
                leftChild = l[ parent*2 + 1 ]
            else :
                leftChild = (-1, -1)
            if  b :
                break;
            parent_i = parent
            parent = l[parent]
            maxChild = max(leftChild, rightChild)
            if maxChild > parent:
                if leftChild == maxChild:
                    self.swap(parent_i*2 + 1, parent_i)
                    parent = parent_i*2 + 1
                elif  rightChild == maxChild:
                    self.swap(parent_i*2 + 2, parent_i)
                    parent = parent_i*2 + 2  
            else:
                break
        return ;
    def swap (self, i, j):
        l = self._arr
        l[i], l[j] = l[j], l[i]
        return 
        

def adjList(n, l):
    '''
    creates the adjacency list in the form of list of dictionaries
    
    in the dictionaries the key corresponds to the node and value 
    corresponds to the capacity 
    '''
    ans = [{} for i in range(n)]
    for edges in l:
        u = edges[0]
        v = edges[1]
        packet = edges[2]
        if v in ans[u]: 
            ans[u][v] = max(ans[u][v], packet)
            ans[v][u] = max(ans[v][u], packet)
        else :
            ans[u][v] = packet
            ans[v][u] = packet
    return ans

def dij(s, t, n, adjList): 
    '''initialising the values 
    capacity is the list that will contain the maximum capacity from 
    the  source node to the target node after its completion '''
    infinity = float('inf')
    capacity = [-1 for i in range(n)]
    p = MaxHeap()
    capacity[s] = 0
    # because infinity capacity can be transferred from the source node 
    # to itself hence the element put in the Max Heap is (infinity, source node)
    #
    # the heap contains element of the form (capacity, node) , where capacity
    # is the maximum data size that can be tranferred till that node starting
    # from the source node 
    p.put((infinity, s))
    sequence = [(s,) for i in range(n)]
    while (not p.empty()): # if Heap is empty then evrything is deduced 
                            # stop the iteration 
        temp = p.get()
        maxCapacity = temp[0]
        tempVertex = temp[1]
        neighbours = adjList[tempVertex]
        
        
        # suppose the capacity at the vertex tempVertex is 'c'
        # then the maximum capacity till the neighbours of tempVertex
        # will be the min of 'c' and the capacity of the edge between them
        # also this value will be accepted only when the already existing 
        # capacity of the neighbourNode is smaller than this value 
        # In that case only we are updating the value to the Heap 
        # and in all other cases we are not updating 
        
        # for getting the sequence of the nodes :
        #     consider the fact that if a neighbourNode's maximum capacity
        #     is updated by the edge from tem vertex then the path to the 
        #     corresponding value comes from the path of the tempVertex and 
        #     then adding the tempVertex to its path. 
        #     This is what we have done.
        #     And as it can be done in O(1) along with all oother comparison
        #     operations in the for loop below 
        #     TC ~ O(m*log(m)) remains intact following from the fact that
        #     Dijkastra Algorithm has been used.
        
        # exactly based on Dijkastra and hence TC ~ O(m*log(m))
        
        
        for x in neighbours:
            d = neighbours[x]
            if (min(maxCapacity, d) > capacity[x]):
                capacity[x] = min(maxCapacity, d)
                p.put((capacity[x], x))
                l = sequence[tempVertex]
                l += (tempVertex,)
                sequence[x] = l
    # final is the path taken to reach the target node 't' 
    # and hence is the 't' th elemnt of the sequence list !
    # similar for capacity[t]            
    final = sequence[t]
    
    # Removing the corner cases that may occour and returning !
    if final[0] != s:
        return 0, [ x for x in ((s,) + final)]
    if s == t:
        return infinity, [s, t]
    if final[0] == final[1]:
        return capacity[t], [x for x in (final[1:] +  (t,))]
    return capacity[t], [ x for x in (final + (t,))]
          
def findMaxCapacity(n, links, s, t):
    # using the functions built above
    l = adjList(n, links)
    return dij(s, t, n, l)
    

# if __name__ == "__main__":
    
#     print (findMaxCapacity(3,[(0,1,1),(1,2,1)],0,1))
#     print (findMaxCapacity(4,[(0,1,30),(0,3,10),(1,2,40),(2,3,50),(0,1,60),(1,3,50)],0,3))
#     print (findMaxCapacity(4,[(0,1,30),(1,2,40),(2,3,50),(0,3,10)],0,3))
#     print (findMaxCapacity(5,[(0,1,3),(1,2,5),(2,3,2),(3,4,3),(4,0,8),(0,3,7),(1,3,4)],0,2))
#     print (findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4), (2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))
#     print (findMaxCapacity(13,[(0,1,100),(0,2,50),(1,5,1),(5,4,50),(1,4,70),(1,3,90),(1,2,15),(2,3,20),(3,4,35),(1,7,10),(2,6,90),(3,7,60),(4,8,10),(5,9,40),(6,7,2),(7,8,40),(8,9,55),(3,10,30),(10,8,5),(10,11,5),(11,9,80),(12,10,60),(6,12,7),(7,12,70)],0,5))