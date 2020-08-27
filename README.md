# SMT-based-Optimal-LTL-Motion-Planning-for-Multi-Robot

Problem statment: </br>
Let us assume that a 2D workspace is divided into small rectangular blocks using a grid. The size of the
workspace is 5 × 5. The lower left grid block has the ID (0, 0), and the upper right grid block has the ID
(4, 4). The blocks (2, 0), (3, 0), (1, 2), (3, 2), (1, 4), and (2, 4) are covered with obstacles. The robots have
motion primitives to perform one-step vertical, horizontal and diagonal movement. A vertical movement and a
horizontal movement incur a cost of 1 unit, and a diagonal movement incurs a cost of 1.5. Each robot has a
motion primitive that keeps it in the same grid block for one time unit. This primitive incurs a cost of 0.5.
Consider the following requirement. The robots have to explore the whole workspace and reach their final
destinations. For a successful exploration, each obstacle-free grid cell should be visited by at least one robot
for at least once. Suppose that the initial location of the robots are (0, 0), (0, 1), (1, 0) and (1, 1) and the final
location of the robots are (0, 0), (0, 4), (4, 0) and (4, 4). The final locations are not assigned to individual robots.
Any robot can go to any of the final locations. Provide an LTL formula that captures the requirement stated
above. A plan for this multi-robot system will be optimal if the total cost for all the movements involved in
the plan is minimal. Formulate the optimal plan generation problem as an SMT-solving problem and generate
a motion plan using Z3 SMT solver. To find the solution iteratively, you should write a script to generate the
Boolean formulas for a specific length of the trajectory automatically. </br>
