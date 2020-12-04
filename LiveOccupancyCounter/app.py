from receiver import receiveCount
from webServer import webserver
from multiprocessing import Process

p2 = Process(target=receiveCount)
p2.start()

p1 = Process(target=webserver)
p1.start()

# and so on
p2.join()
p1.join()

# the join means wait untill it finished