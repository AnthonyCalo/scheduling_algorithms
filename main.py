#AUTHOR: ANTHONY CALO JR.

import json
from collections import defaultdict
import heapq
import statistics
import copy
import random
from abc import ABC, abstractmethod



def check_job(job):
    return job["cycles"]>0

#base class        
class ScheduleAlg(ABC):
    def __init__(self, jobs):
        self.total_time = 0
        self.time_dict = defaultdict(int)
        self.jobs = copy.deepcopy(jobs)
        self.typename = ""

    @abstractmethod
    def run(self):
        pass

   
    def calculate_average_throughput(self):
        mean = statistics.mean(self.time_dict.values())    
        print("Average throughput for {} algorithm is {}".format(self.typename, mean))
        return mean
        

class RoundRobin(ScheduleAlg):
    def __init__(self, jobs):
        super().__init__(jobs)
        self.typename = "Round Robin"
    
    def run(self, quantum):
        #While there are still jobs left. Loop over the jobs and execute the quantum amount for each of the remaining jobs
        while len(self.jobs) > 0:
            for job in self.jobs:
                print(job["name"], end=" ")
                time_allocated_for_job = min(quantum, job["cycles"])
                self.total_time += time_allocated_for_job
                job["cycles"] -= time_allocated_for_job
                self.time_dict[job["name"]] = self.total_time
                if(job["cycles"] == 0):
                    print("\nCompleted job {} at time: {}\n".format(job["name"], self.time_dict[job["name"]]))
            #This line removes the completed jobs from the list
            self.jobs = list(filter(check_job, self.jobs))
        return self.time_dict

    


class SPN(ScheduleAlg):
    def __init__(self, jobs):
        super().__init__(jobs)
        self.typename = "Shortest Process Next"

    
    def run(self):
        #sort the jobs. Then loop over and execute them
        self.jobs = sorted(self.jobs, key = lambda x: x["cycles"])
        for job in self.jobs:
            self.total_time += job["cycles"]
            self.time_dict[job["name"]] = self.total_time
            print("Finished executing job {} at time: {}".format(job["name"], self.total_time))


class PriorityQueue(ScheduleAlg):
    def __init__(self, jobs):
        super().__init__(jobs)
        self.typename = "Priority Queue"
        

    def run(self):
        #use a heap and push the job along with the priority
        heap = []
        for job in self.jobs:
            priority = random.randrange(1, 4)
            heapq.heappush(heap, (priority,job["name"], job))
        
        while heap:
            #take the job with the highest priority out of the heap
            priority, name, job = heapq.heappop(heap)
            print("Executing job {} with priority {}".format(name, priority))
            self.total_time += job["cycles"]
            self.time_dict[job["name"]] = self.total_time
        print("Completed priority queue")


def main():
    with open("./jobs.json") as f:
        file_content = f.read()

    # Load the JSON data from the file content
        data = json.loads(file_content)
        f.close()


    dc = data[:]
    rr = RoundRobin(data[:])
    print("Running the round robin algorithm")
    rr.run(25)
    rr.calculate_average_throughput()

    spn = SPN(dc)
    print("\n\nRunning the shortest process next algorithm")
    spn.run()
    print(spn.calculate_average_throughput())

    print("\n\nRunning the priority queue next algorithm")
    pq = PriorityQueue(dc)
    pq.run()
    pq.calculate_average_throughput()

if __name__ == '__main__':
    main()