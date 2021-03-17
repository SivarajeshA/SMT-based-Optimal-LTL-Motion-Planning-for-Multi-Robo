from z3 import *
import random
import sys
import time

N = 5
HOPS=15

# X is a three dimensional grid containing (t, x, y)
X =  [ [ [ Bool("s_%s_%s_%s" % (k, i, j)) for j in range(N) ] for i in range(N) ]  for k in range(HOPS+1)]
s = Solver()

# Start and Goal states
start_state = [0,2]
goal_state = [3,4]

#Generate Random Obstacle
nObs=3
obs = []
# random.seed("CPSL ICRA19")
# for i in range(nObs):
#     x = random.randint(0,N-1)
#     y = random.randint(0,N-1)
#     if ((x==start_state[0] and y == start_state[1]) or (x==goal_state[0] and y==goal_state[1]))== False:  #To avoid obstacles in start and goal state
#         obs.append([x,y])
# #Manual obs        
# obs += [[3,4]]
print("Generated Obstacles",obs)

#Min HOPs required btw start and goal states
#If Diagonal movements are allowed
min_HOP=max(abs(start_state[0]-goal_state[0]),abs(start_state[1]-goal_state[1]))
print("min_Hops",min_HOP)

if(HOPS<min_HOP):
    print("No. of hops are too low")
    exit(1)

# Initial State Constraint
s.add(X[0][start_state[0]][start_state[1]])
#s.add([Not(cell) for row in X[0] for cell in row][1:])

# Goal constraint
# s.add(X[min_HOP][goal_state[0]][goal_state[1]])
# s.add([Not(cell) for row in X[HOPS] for cell in row][:-1])

#Adding Obstacles into solver
for o in obs:
    for t in range(HOPS):
        s.add(Not(X[t][o[0]][o[1]]))

#Sanity Constraints
for grid in X:
    for i in range(len(grid)):
        for j in range(len(grid)):
            for p in range(len(grid)):
                for q in range(len(grid)):
                    if not (i==p and j==q):
                        s.add(Not(And(grid[i][j], grid[p][q])))      

#Motion primitives
for t in range(HOPS):
    for x in range(N):
        for y in range(N):
            temp = Or(X[t][x][y])
            #Vertical Movements
            if (x+1 < N):
                temp = Or(temp, X[t][x+1][y])
            if (y+1 < N):
                temp = Or(temp, X[t][x][y+1])
            #Horizontal Movements
            if (x-1 >= 0):
                temp = Or(temp, X[t][x-1][y])
            if (y-1 >= 0):
                temp = Or(temp, X[t][x][y-1])
            # #Diagonal Movements
            # if((x+1 < N) and (y+1 < N)):
            #     temp = Or(temp, X[t][x+1][y+1])
            # if((x-1 < N) and (y-1 < N)):
            #     temp = Or(temp, X[t][x-1][y-1])
            # if((x+1 < N) and (y-1 < N)):
            #     temp = Or(temp, X[t][x+1][y-1])
            # if((x-1 < N) and (y+1 < N)):
            #     temp = Or(temp, X[t][x-1][y+1])
            s.add(simplify(Implies(X[t+1][x][y], temp)))

start_time = time.time()
path = []
while(True):
    s.push()
    # Goal state constraint
    s.add(X[min_HOP][goal_state[0]][goal_state[1]])
    
    #SAT
    if s.check() == sat:
        print("Path synthesized as follows...(s_t_x_y)")
        m = s.model()
        for t in range(min_HOP+1):
            for x in range(N):
                for y in range(N):
                    if m.evaluate(X[t][x][y]):
                        #print(X[t][x][y])
                        print('[',x,',',y,']')
                        path.append([x,y])
        print("No. of Hops taken",min_HOP)
        break
    s.pop()
    #Increment min_HOP, if not SAT 
    min_HOP +=1
    if(min_HOP>HOPS):
        print("Given hops limit is too low to find a path...")
        exit(1)

#Calculate time
t=time.time() - start_time

#Find Action from state transition
def findAction(s1,s2):
    x1=int(s1[0])
    y1=int(s1[1])
    x2=int(s2[0])
    y2=int(s2[1])
    if x1==x2 and y1<y2:
        return 'U'
    if x1==x2 and y1>y2:
        return 'D'
    if x1>x2 and y1==y2:
        return 'L'
    if x1<x2 and y1==y2:
        return 'R'
    else:
        return 'X'
action =[]
for i in range(len(path)-1):
    action.append(findAction(path[i],path[i+1]))
print("Actions Taken: ",action)
print("Time taken : %s seconds" % t)
print("---------------Done---------------")