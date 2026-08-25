# EE673 — Digital Communication Networks Projects

This repository contains three EE673 assignment projects, each combining theory with practical networking work.

- **Project 1: Socket Programming and Application Protocols (Python)**
  - Built TCP and UDP client-server programs using Python's `socket` module for reliable and connectionless communication.
  - Implemented a threaded UDP peer chat tool with live send/receive behavior (`threading`, `socket`), designed for real network use across devices.
  - Developed an interactive SMTP client from raw protocol commands, including secure login flows (`ssl`/STARTTLS), authentication, and MIME attachments (`email` package).

- **Project 2: Protocol Analysis, Congestion Control, and Throughput Evaluation**
  - Performed packet-level protocol analysis using **Wireshark** for UDP/TCP/IP behavior and header-level reasoning.
  - Compared TCP congestion control variants (**Old Tahoe, Reno, Cubic**) in **NetSim**, with clear analysis of window dynamics and link utilization under loss.
  - Measured real network bandwidth using **iPerf3**, translating experimental output into actionable performance observations.

- **Project 3: Routing Algorithms and Network-Layer Analysis**
  - Implemented **Link-State routing** using Dijkstra's algorithm (`heapq`) to generate shortest-path routing tables for all nodes.
  - Implemented a **Distance-Vector routing** simulation (Bellman-Ford style) with iterative neighbor updates and convergence tracking.
  - Complemented implementations with protocol-focused written analysis (ICMP, traceroute, and IP-layer behavior) in the submitted report.