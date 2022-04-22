#!/usr/bin/env python3
import sys, getopt

def sortByArrival(e):
   return e['arrival']

def sortByNum(e):
   return e['num']

def sortByTimeLeft(e):
   return e['run'] - e['ran']

def printTimes(finished):
   totalWait = 0
   totalTurn = 0
   finished.sort(key=sortByNum)
   for job in finished:
      turnTime = job['fin'] - job['arrival']
      print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (job['num'], turnTime, job['wait']))
      totalTurn += turnTime
      totalWait += job['wait']
   totalTurn /= float(len(finished))
   totalWait /= float(len(finished))
   print("Average -- Turnaround %3.2f  Wait %3.2f" % (totalTurn, totalWait))

def fifo(jobs):
   currTime = 0
   totalWait = 0
   totalTurn = 0
   #totalTime
   for job in jobs:
      if currTime < job['arrival']:
         currTime = job['arrival']
      waitTime = currTime - job['arrival']
      currTime += job['run']
      turnAround = currTime - job['arrival']
      print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (job['num'], turnAround, waitTime))
      totalWait += waitTime
      totalTurn += turnAround
   totalTurn /= float(len(jobs))
   totalWait /= float(len(jobs))
   print("Average -- Turnaround %3.2f  Wait %3.2f" % (totalTurn, totalWait))
   return

def srtn(jobs):
   finished = []
   currTime = 0
   availJobs = []
   while len(jobs) > 0 or len(availJobs) > 0:
      if len(availJobs) == 0:
         currTime = jobs[0]['arrival']
      while len(jobs) > 0 and jobs[0]['arrival'] <= currTime:
         job = jobs.pop(0)
         job['ran'] = 0
         job['wait'] = 0
         availJobs.append(job)
      availJobs.sort(key=sortByTimeLeft)
      currJob = availJobs.pop(0)
      for job in availJobs:
         job['wait'] += 1
      currJob['ran'] += 1
      currTime+=1
      if currJob['ran'] == currJob['run']:
         currJob['fin'] = currTime
         finished.append(currJob)
      else:
         availJobs.append(currJob)
   printTimes(finished)
   
def rr(jobs, q):
   availJobs = []
   finished = []
   currTime = 0
   cycle = 0
   while len(jobs) > 0 or len(availJobs) > 0:
      if len(availJobs) == 0:
         currTime = jobs[0]['arrival']
         cycle = 0
      while len(jobs) > 0 and jobs[0]['arrival'] <= currTime:
         job = jobs.pop(0)
         job['ran'] = 0
         job['wait'] = 0
         availJobs.append(job)
      currJob = availJobs.pop(0)
      for job in availJobs:
         job['wait'] += 1
      currJob['ran'] += 1
      #print("ran job %d" % currJob['num'])
      currTime+=1
      if currJob['ran'] == currJob['run']:
         currJob['fin'] = currTime
         finished.append(currJob)
         cycle = 0
      else:
         cycle = (cycle + 1)%q
         if cycle == 0:
            availJobs.append(currJob)
         else:
            availJobs.insert(0, currJob)
      #print("cycle : %d" % cycle)
      #print(currJob)
      #print(jobs)
      #print(availJobs)
      #print(finished)
   printTimes(finished)
      

def main(argv):
   infile = argv[1]
   stype = 0
   q = 1

   #assess command line arguments
   argi = argv[2:]
   try:
      opts, args = getopt.getopt(argi,"p:q:")
   except getopt.GetoptError:
      print('schedSim <job-file.txt> -p <ALGORITHM> -q <QUANTUM>')
      sys.exit(2)
    
   for opt, arg in opts:
      if opt == '-p':
         if arg in ('SRTN', 'srtn'):
            stype = 1
         elif arg in ('RR', 'rr'):
            stype = 2
      elif opt == '-q':
            q = int(arg)
   #print(stype, q)

   #read in job tuples
   jobs = []
   file = open(infile, 'r')
   lines = file.readlines()
   for line in lines:
      chars = line.split()
      if len(chars) != 2:
         print('Error: textfile is not formatted correctly')
         sys.exit(2)
      jobs.append({'run' : int(chars[0]), 'arrival' : int(chars[1])})
   #print(jobs)
   jobs.sort(key=sortByArrival)
   #assign job numbers
   for i in range(0, len(jobs)):
      jobs[i]['num'] = i
   #execute based on stype
   if stype == 0:
      fifo(jobs)
   elif stype == 1:
      srtn(jobs)
   else:
      rr(jobs, q)
   
   file.close()

if __name__ == "__main__":
   main(sys.argv)