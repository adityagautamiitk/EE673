import copy

# Global event queue to simulate the network layer passing packets
event_queue = []

def tolayer2(packet):
    """Simulates sending a routing packet to a directly connected neighbor."""
    event_queue.append(packet)

class RTPkt:
    """Format for the communication packet."""
    def __init__(self, sourceid, destid, mincost):
        self.sourceid = sourceid  
        self.destid = destid      
        self.mincost = copy.deepcopy(mincost) 

class DVNode:
    """Maintains the state and logic for a Distance-Vector Node."""
    def __init__(self, node_id, neighbors):
        self.id = node_id
        self.num_nodes = 4
        self.INFINITY = 999
        
        self.neighbors = neighbors 
        self.min_costs = [self.INFINITY] * self.num_nodes
        self.min_costs[self.id] = 0
        
        self.dt = [[self.INFINITY] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            self.dt[i][self.id] = 0
            
        self.next_hop = [-1] * self.num_nodes
        self.next_hop[self.id] = self.id

    def init_node(self):
        """Initializes distance table with direct costs and notifies neighbors."""
        for nbr, cost in self.neighbors.items():
            self.min_costs[nbr] = cost
            self.dt[nbr][nbr] = cost
            self.next_hop[nbr] = nbr
        self.notify_neighbors()

    def notify_neighbors(self):
        """Creates an rtpkt and sends it to all directly connected neighbors."""
        for nbr in self.neighbors.keys():
            pkt = RTPkt(sourceid=self.id, destid=nbr, mincost=self.min_costs)
            tolayer2(pkt)

    def update_node(self, rtpkt):
        """Updates the distance table based on a received routing packet."""
        src = rtpkt.sourceid
        changed = False
        
        for dest in range(self.num_nodes):
            new_cost = self.neighbors[src] + rtpkt.mincost[dest]
            if new_cost < self.dt[dest][src]:
                self.dt[dest][src] = new_cost
        
        for dest in range(self.num_nodes):
            current_min = self.INFINITY
            best_hop = -1
            
            for nbr in self.neighbors.keys():
                if self.dt[dest][nbr] < current_min:
                    current_min = self.dt[dest][nbr]
                    best_hop = nbr
                    
            if current_min < self.min_costs[dest]:
                self.min_costs[dest] = current_min
                self.next_hop[dest] = best_hop
                changed = True
                
        if changed:
            self.notify_neighbors()


# --- Node Instantiations based on the Network Graph ---
nodes = {
    0: DVNode(0, {1: 1, 2: 3, 3: 7}),
    1: DVNode(1, {0: 1, 2: 1}),
    2: DVNode(2, {0: 3, 1: 1, 3: 2}),
    3: DVNode(3, {0: 7, 2: 2})
}

# --- Required Routines defined in the Assignment ---
def rtinit0(): nodes[0].init_node()
def rtinit1(): nodes[1].init_node()
def rtinit2(): nodes[2].init_node()
def rtinit3(): nodes[3].init_node()

def rtupdate0(pkt): nodes[0].update_node(pkt)
def rtupdate1(pkt): nodes[1].update_node(pkt)
def rtupdate2(pkt): nodes[2].update_node(pkt)
def rtupdate3(pkt): nodes[3].update_node(pkt)


def main():
    print("Initializing Distance-Vector Routing...")
    
    rtinit0()
    rtinit1()
    rtinit2()
    rtinit3()
    
    # Process packets until the network converges
    packet_count = 0
    while event_queue:
        pkt = event_queue.pop(0)
        packet_count += 1
        
        if pkt.destid == 0: rtupdate0(pkt)
        elif pkt.destid == 1: rtupdate1(pkt)
        elif pkt.destid == 2: rtupdate2(pkt)
        elif pkt.destid == 3: rtupdate3(pkt)
        
    print(f"Network converged after exchanging {packet_count} routing packets.\n")
    print("Final Routing Tables:")
    print("="*45)
    
    for i in range(4):
        print(f"Routing Table for Node {i}:")
        print(f"{'Destination':<15} | {'Total Cost':<12} | {'Next Hop':<10}")
        print("-" * 45)
        for dest in range(4):
            cost = nodes[i].min_costs[dest]
            next_hop = nodes[i].next_hop[dest] if dest != i else "-"
            print(f"Node {dest:<10} | {cost:<12} | {next_hop}")
        print("\n")

if __name__ == "__main__":
    main()
