# SDN-Based Access Control System using POX and Mininet

## Problem Statement
To design and implement an SDN-based access control system that allows only authorized hosts to communicate within a network using a whitelist policy.

---

##  Objective
- Implement controller–switch interaction using OpenFlow
- Design match–action flow rules
- Enforce access control using whitelist
- Demonstrate behavior using ping and iperf
- Validate policy consistency

---

##  Technologies Used
- Mininet
- POX Controller
- Open vSwitch
- Python
- iperf
- Wireshark (optional)

---

##  Network Topology

Star topology with one switch and four hosts:

h1   h2   h3   h4  
 \    |    |    /  
        s1  

---

##  Project Structure

sdn_access_control/  
├── access_topology.py  
├── whitelist.txt  

pox/pox/misc/  
└── access_control.py  

---

##  Whitelist Policy

Only the following host pairs are allowed:

00:00:00:00:00:01 → 00:00:00:00:00:02  
00:00:00:00:00:02 → 00:00:00:00:00:01  
00:00:00:00:00:02 → 00:00:00:00:00:03  
00:00:00:00:00:03 → 00:00:00:00:00:02  

All other communication is blocked.

---

##  Setup and Execution

### Step 1: Start POX Controller
cd ~/pox  
python3 pox.py misc.access_control  

---

### Step 2: Run Mininet Topology
cd ~/sdn_access_control  
sudo mn --custom access_topology.py --topo mytopo --controller remote  

---
##  Test Scenarios

###  Allowed Communication
h1 ping -c 5 h2  

Result: Successful (0% packet loss)

---

###  Blocked Communication
h1 ping -c 5 h4  

Result: Failed (100% packet loss)

---

##  Throughput Testing (iperf)

### Allowed Case
h2 iperf -s &  
h1 iperf -c h2  

Result: High throughput (~10 Gbps)

---

### Blocked Case
h4 iperf -c h2  

Result: Connection fails

---

## Flow Table Verification

sudo ovs-ofctl dump-flows s1  

Shows:
- Allow rules (FLOOD)
- Drop rules (blocked traffic)

---

##  Observations

- First packet is sent to controller (PacketIn)
- Controller installs flow rules dynamically
- Allowed traffic flows normally after rule installation
- Unauthorized traffic is consistently blocked

---

##  Regression Testing & Policy Consistency

- Allowed communication remains successful across repeated tests
- Blocked communication consistently fails
- iperf confirms enforcement at application level

---

##  Proof of Execution

Include screenshots of:
- Mininet topology (nodes)
- Allowed ping
- Blocked ping
- Controller logs
- Flow table output
- iperf results
- Wireshark capture (optional)

---

##  Conclusion

The project successfully demonstrates SDN-based access control using a centralized controller. The controller dynamically installs flow rules in the switch based on whitelist policies, ensuring secure and controlled communication.

---

##  References

- Mininet Documentation
- POX Controller Documentation
- OpenFlow Specification