# TMA_Project_SDN_DDoS
TMA project carried out by Murad Al-Smady, Gulzar Hacizade, Roger Sans Falip, Luca Stroppa, and Arnold Veltmann. This project aims to provide a solution against DDoS attacks in an SDN environment.


### Instructions on how to run

1. Install mininet
```bash
sudo apt-get install mininet
```

2. Install python and pip
```bash
sudo apt-get install python2 python3 python3-pip
```
3. To prevent ryu and mininet erros install a specific version of eventlet
```bash
pip install eventlet==0.30.2
```
4. Install ryu
```bash
pip3 install ryu
```
5. To erase the cache from mininet run
```bash
sudo mn -c
```

6. To start the controller run
```bash
ryu-manager controller.py
```

7. To start the mininet topology and the attacks run

```bash
sudo python2 topo.py
```
