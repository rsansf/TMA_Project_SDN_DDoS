#!/usr/bin/python
from time import sleep

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo

TEST_TIME = 300  # seconds


class DDoSTopology(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        h_list = []
        for i in range(1, 11):
            h = 'h{}'.format(i)
            ip = '10.0.0.{}/24'.format(i)
            mac = '00:00:00:00:00:0{}'.format(i)

            new_h = self.addHost(h, ip=ip, mac=mac)
            h_list.append(new_h)

        for h in h_list:
            self.addLink(h, s1, cls=TCLink, bw=50)


if __name__ == '__main__':
    setLogLevel('info')
    topo = DDoSTopology()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()

    normal_command = 'bash normal.sh &'
    attack_command = 'bash attack.sh &'

    h1 = net.get('h1')
    h1.cmd(normal_command)

    h2 = net.get('h2')
    h2.cmd(normal_command)

    h3 = net.get('h3')
    h3.cmd(normal_command)

    h4 = net.get('h4')
    h4.cmd(attack_command)

    h5 = net.get('h5')
    h5.cmd(normal_command)

    h6 = net.get('h6')
    h6.cmd(normal_command)

    h7 = net.get('h7')
    h7.cmd(attack_command)

    h8 = net.get('h8')
    h8.cmd(normal_command)

    h9 = net.get('h9')
    h9.cmd(normal_command)

    h10 = net.get('h10')
    h10.cmd(attack_command)

    sleep(TEST_TIME)
    net.stop()
