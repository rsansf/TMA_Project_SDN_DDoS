# TMA_Project_SDN_DDoS
TMA project carried out by Murad Al-Smady, Gulzar Hacizade, Roger Sans Falip, Luca Stroppa, and Arnold Veltmann. The aim of this project is to provide a solution against DDoS attacks in an SDN environment.


HOW TO RUN IT:
1. sudo apt-get install mininet
2. sudo apt-get install python2 python3 python3-pip
3. pip install eventlet==0.30.2
4. pip3 install ryu
5. sudo mn -c //to erase cache stored stuff from mininet
6. ryu-manager controller.py //to start the controller
7. sudo python2 topo.py //to start the mininet topology and the attacks

