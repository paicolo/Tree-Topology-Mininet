#!/usr/bin/env python
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology(args):

    net = Mininet_wifi()

    info("* Creating nodes\n")
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='192.168.10.2/24' )
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='192.168.10.3/24', range='20' )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'pai1-ssid', mode= 'g', channel= '1', position='150,20,0', range='30' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'pai2-ssid', mode= 'g', channel= '1', position='30,220,0', range='30' )
    ap3 = net.addAccessPoint( 'ap3', ssid= 'pai3-ssid', mode= 'g', channel= '1', position='150,280,0', range='30' )
    ap4 = net.addAccessPoint( 'ap4', ssid= 'pai4-ssid', mode= 'g', channel= '1', position='280,230,0', range='30' )
    ap5 = net.addAccessPoint( 'ap5', ssid= 'pai5-ssid', mode= 'g', channel= '1', position='130,50,0', range='30' )
    c1 = net.addController( 'c1' )

    info("* Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("* Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("* Associating and Creating links\n")
    net.addLink(ap1, h1)
    net.addLink(ap1, ap5)
    net.addLink(ap5, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)
    net.addLink(ap4, ap5)

    if '-p' not in args:
        net.plotGraph(max_x=300, max_y=300)

    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=300, max_y=300, seed=20)
    
    info("* Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])

    info("* Running CLI\n")
    CLI( net )

    info("* Stopping network\n")
    net.stop()

if _name_ == '_main_':
    setLogLevel( 'info' )
    topology(sys.argv)