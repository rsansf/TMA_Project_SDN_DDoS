#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet, Host
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from time import sleep

TEST_TIME = 300 #seconds

class DDoSTopology(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', ip='10.0.0.3/24', mac="00:00:00:00:00:03")
        h4 = self.addHost('h4', ip='10.0.0.4/24', mac="00:00:00:00:00:04")
        h5 = self.addHost('h5', ip='10.0.0.5/24', mac="00:00:00:00:00:05")
        h6 = self.addHost('h6', ip='10.0.0.6/24', mac="00:00:00:00:00:06")
        h7 = self.addHost('h7', ip='10.0.0.7/24', mac="00:00:00:00:00:07")
        h8 = self.addHost('h8', ip='10.0.0.8/24', mac="00:00:00:00:00:08")
        h9 = self.addHost('h9', ip='10.0.0.9/24', mac="00:00:00:00:00:09")
        h10 = self.addHost('h10', ip='10.0.0.10/24', mac="00:00:00:00:00:10")


        self.addLink(h1, s1, cls=TCLink, bw=50)
        self.addLink(h2, s1, cls=TCLink, bw=50)
        self.addLink(h3, s1, cls=TCLink, bw=50)
        self.addLink(h4, s1, cls=TCLink, bw=50)
        self.addLink(h5, s1, cls=TCLink, bw=50)
        self.addLink(h6, s1, cls=TCLink, bw=50)
        self.addLink(h7, s1, cls=TCLink, bw=50)
        self.addLink(h8, s1, cls=TCLink, bw=50)
        self.addLink(h9, s1, cls=TCLink, bw=50)
        self.addLink(h10, s1, cls=TCLink, bw=50)

if __name__ == '__main__':
    setLogLevel('info')
    topo = DDoSTopology()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()

    h1 = net.get('h1')
    cmd1 = "bash normal.sh &"
    h1.cmd(cmd1)

    h2 = net.get('h2')
    cmd1 = "bash normal.sh &"
    h2.cmd(cmd1)

    h3 = net.get('h3')
    cmd1 = "bash normal.sh &"
    h3.cmd(cmd1)

    h4 = net.get('h4')
    cmd1 = "bash attack.sh &"
    h4.cmd(cmd1)

    h5 = net.get('h5')
    cmd1 = "bash normal.sh &"
    h5.cmd(cmd1)

    h6 = net.get('h6')
    cmd1 = "bash normal.sh &"
    h6.cmd(cmd1)

    h7 = net.get('h7')
    cmd1 = "bash attack.sh &"
    h7.cmd(cmd1)

    h8 = net.get('h8')
    cmd1 = "bash normal.sh &"
    h8.cmd(cmd1)

    h9 = net.get('h9')
    cmd1 = "bash normal.sh &"
    h9.cmd(cmd1)

    h10 = net.get('h10')
    cmd1 = "bash attack.sh &"
    h10.cmd(cmd1)


    sleep(TEST_TIME)
    net.stop()

