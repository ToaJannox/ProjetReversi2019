from threading import Thread
from queue import Queue
import time

exitFlag = 0



def f(i,queue):
   res = i+1
   queue.put(res)

queue = Queue()   
thread_res = []
for i in range(0,10):
   print(i)
   thread = Thread(target=f,name="super Thread",args=[i,queue])
   thread.start()
   response = queue.get()
   thread_res.append(response)

for i in range (0,10):
   thread.join()

   
print("thread result ",thread_res)


l = [(2,1),(5,4),(2,7)]

print(l)
