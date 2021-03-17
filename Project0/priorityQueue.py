import heapq

class PriorityQueue():
    def __init__(self):
        self.pq = []        # list of entries arranged in priority queue
        self.count = 0      # counter of items in priority queue

    def push(self, item, priority):
        for i in range(0, self.count):          #Loop through priority queue
            if item == self.pq[i][1]:           #If item already exists in priority queue, return False
                return False
        self.count += 1     #increment count
        heapq.heappush(self.pq, (priority, item))   #push the item in min-heap
        return True

    def pop(self):
        self.count -= 1     #decrement count
        return heapq.heappop(self.pq)[1]    #return the item popped by min-heap

    def isEmpty(self):
        if self.count == 0: return True
        else: return False

    def update(self, item, priority):
        flag = False                            #flag to declare existence of item in priority queue
        for i in range(0, self.count):          #Loop through priority queue
            if item == self.pq[i][1]:           #If item already exists in priority queue
                if priority < self.pq[i][0]:    #Check if given priority is smaller
                    q = (list)(self.pq)         #Tuples can't change their items -> convert into list
                    q.pop(i)                    #Pop the specified index
                    self.pq = q
                    self.count -= 1             #Decrement count because push increments count
                    self.push(item, priority)   #Push item with given priority
                else: pass
                flag = True                     #flag is True because item was already in priority queue
                break
            else: pass
        if not flag:                            #If item not in priority queue, push
            self.push(item, priority)

    def printPQ(self):
        print(self.pq)

def PQSort(list):
    q = PriorityQueue()         #Create priority queue
    for x in list:              #Push every item of list in priority queue
        q.push(x, x)
    list.clear()                #Clear list
    while q.count > 0:          #Append every item of priority queue in list
        list.append(q.pop())
    return list