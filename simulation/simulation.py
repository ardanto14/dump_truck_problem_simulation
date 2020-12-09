import heapq
import random

# Node class 
class Node: 
        # Function to initialize the node object 
    def __init__(self, data): 
        self.data = data    # Assign data 
        self.next = None    # Initialize    
     
# Linked List class 
class LinkedList: 
         
    # Function to initialize the Linked    
    # List object 
    def __init__(self):    
        self.head = None
        self.tail = None
        self.length = 0

    def insert(self, obj):

        if self.tail is None and self.head is None:
            self.tail = Node(obj)
            self.head = self.tail

        else:
            new_node = Node(obj)
            self.tail.next = new_node
            self.tail = new_node

        self.length += 1

    def pop(self):
        if self.head is None:
            raise IndexError
        
        if self.head == self.tail:
            returned = self.head.data

            self.head = None
            self.tail = None

            self.length = 0

            return returned
        
        returned = self.head
        self.head = self.head.next

        self.length -= 1
        
        return returned.data

    def to_list(self):
        returned = []

        current = self.head
        while current is not None:
            returned.append(current.data)
            current = current.next
            
        return returned

class Truck:
    def __init__(self, id):
        self.id = id


class Server:
    def __init__(self, delay_list):
        self.delay_list = delay_list
        self.delay_list_length = len(self.delay_list)
        self.id_now = 0
        self.serving = 0
        self.busy_time = 0
        

    def get_delay(self):
        returned = self.delay_list[self.id_now]
        self.id_now += 1

        if self.id_now > self.delay_list_length - 1:
            self.id_now = 0

        return returned
        

class Event:
    def __init__(self, id, t, truck):
        self.id = id
        self.t = t
        self.truck = truck

    def __lt__(self, other):
        return self.t < other.t


class DumpTruckSimulator():

    def __init__(self, loader_queue_count, scaler_queue_count):
        self.loader_queue_count = loader_queue_count
        self.scaler_queue_count = scaler_queue_count



    def run_simulation(self, num_event):
        future_event_list = []

        heapq.heapify(future_event_list)

        loader_queue = LinkedList()
        scaler_queue = LinkedList()
        truck_list = [None, None, None, None, None, None]

        for i in range(6):
            truck_list[i] = Truck('DT' + str(i))

        
        for i in range(self.loader_queue_count):
            loader_queue.insert(Truck('DT' + str(i)))

        for i in range(self.loader_queue_count, self.loader_queue_count + self.scaler_queue_count):
            scaler_queue.insert(Truck('DT' + str(i)))

        
        

        scaler_queue.insert(truck_list[5])

        loader1 = Server([10, 5, 5, 10, 15, 10, 10])
        loader2 = Server([10, 5, 5, 10, 15, 10, 10])
        scaler = Server([12, 12, 12, 16, 12, 16])
        travel = Server([60, 100, 40, 40, 80])

        if loader_queue.length > 0 and loader1.serving == 0:
            truck = loader_queue.pop()
            heapq.heappush(future_event_list, Event('DL1', loader1.get_delay(), truck))
            loader1.serving += 1
                    
        if loader_queue.length > 0 and loader2.serving == 0:
            truck = loader_queue.pop()
            heapq.heappush(future_event_list, Event('DL2', loader2.get_delay(), truck))
            loader2.serving += 1

        if scaler_queue.length > 0 and scaler.serving == 0:
            truck = scaler_queue.pop()
            heapq.heappush(future_event_list, Event('DS', scaler.get_delay(), truck))
            scaler.serving += 1

        result = []

        result.append([0,
                loader_queue.length,
                loader1.serving,
                loader2.serving,
                scaler_queue.length,
                scaler.serving,
                travel.serving,
                loader_queue.to_list(),
                scaler_queue.to_list(),
                future_event_list.copy(),
                loader1.busy_time,
                loader2.busy_time,
                scaler.busy_time])


        for i in range(0, num_event-1):

            event = heapq.heappop(future_event_list)


            if loader1.serving > 0:
                loader1.busy_time += event.t - result[-1][0]

            if loader2.serving > 0:
                loader2.busy_time += event.t - result[-1][0]

            if scaler.serving > 0:
                scaler.busy_time += event.t - result[-1][0]


            if event.id == 'AL':
                loader_queue.insert(event.truck)
                travel.serving -= 1

            elif event.id == 'DL1':
                loader1.serving -= 1
                scaler_queue.insert(event.truck)

            elif event.id == 'DL2':
                loader2.serving -= 1
                scaler_queue.insert(event.truck)
                
            elif event.id == 'DS':
                scaler.serving -= 1
                heapq.heappush(future_event_list, Event('AL', event.t + travel.get_delay(), event.truck))
                travel.serving += 1


            if loader_queue.length > 0 and loader1.serving == 0:
                truck = loader_queue.pop()
                heapq.heappush(future_event_list, Event('DL1', event.t + loader1.get_delay(), truck))
                loader1.serving += 1
                    
            if loader_queue.length > 0 and loader2.serving == 0:
                truck = loader_queue.pop()
                heapq.heappush(future_event_list, Event('DL2', event.t + loader2.get_delay(), truck))
                loader2.serving += 1

            if scaler_queue.length > 0 and scaler.serving == 0:
                truck = scaler_queue.pop()
                heapq.heappush(future_event_list, Event('DS', event.t + scaler.get_delay(), truck))
                scaler.serving += 1

            


            
            result.append([event.t,
                loader_queue.length,
                loader1.serving,
                loader2.serving,
                scaler_queue.length,
                scaler.serving,
                travel.serving,
                loader_queue.to_list(),
                scaler_queue.to_list(),
                future_event_list.copy(),
                loader1.busy_time,
                loader2.busy_time,
                scaler.busy_time])

        return result

        
