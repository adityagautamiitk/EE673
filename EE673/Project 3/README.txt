EE673 Assignment 3 Submission

Submitted by Aditya Gautam, 220064

Question 1 & Question 3: Please check the attached "Q1 and Q3 Answers.pdf" file.

Question 2: Centralized and Distributed Routing Algorithms

This section contains the implementations for the Link-State (Centralized) and Distance-Vector (Distributed) routing algorithms for the network topology provided in the graph given in the PS.

1. Link-State (LS) Routing Algorithm
File: ls_routing.py
Description: Implements Dijkstra's algorithm to compute the shortest path. It assumes global network knowledge and calculates the minimum cost and next-hop routing table for every node in the graph.
How to run: Open a terminal and execute the following command:
  python ls_routing.py
  (Alternatively, use python3 ls_routing.py depending on your environment).
Output: Prints the complete routing table (Destination, Total Cost, Next Hop) for nodes 0, 1, 2, and 3.

2. Distance-Vector (DV) Routing Algorithm (Optional)
File: dv_routing.py
Description: Implements the distributed Bellman-Ford algorithm. Nodes start with only the costs of directly attached links (rtinit routines) and iteratively exchange routing packets (rtpkt) with immediate neighbors using rtupdate routines until the network tables converge.
How to run: Open a terminal and execute the following command:
  python dv_routing.py
Output: Simulates the packet exchange and prints the final, converged routing tables for all nodes.
