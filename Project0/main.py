from priorityQueue import PriorityQueue, PQSort
from random import seed
from random import randint
import time

print("\n----------test 1----------\n")
pq = PriorityQueue()
pq.push('hello',4)
pq.push('hey',2)
pq.push('hey', 7)
pq.push('wazaa',1)
pq.push('opp',5)

pq.printPQ()
pq.update('hello',1)
pq.printPQ()


print("\n\n----------test 2----------\n")
seed(int(round(time.time() * 1000)))
print( 
    PQSort([randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100)])
)


print("\n\n----------test 3----------\n")
p1 = PriorityQueue()
p1.push('Ihamod',100)
p1.push('Gouno',1)
p1.push('Paschalis',2)
p1.push('Xergias',2000)
while(p1.isEmpty()==False):
    print(p1.pop())

print("\n\n----------test 4----------\n")
q = PriorityQueue()
q.push("task1", 1)
q.push("task1", 2)
q.push("task0", 0)
print(q.pop())
print(q.pop())
q.push("task3", 3)
q.push("task3", 4)
q.push("task2", 0)
print(q.pop())