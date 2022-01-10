from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import DEAD_DISPATCHER
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
from ryu.ofproto import ofproto_v1_3


class controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(controller, self).__init__(*args, **kwargs)
        self._server_ip = '10.0.0.1'
        self._mac_to_port = {}
        self._datapaths = {}
        self._banned_ips = []

        self._spawn_thread()
        self._request = [0] * 20
        self._diff = [0] * 20

    def _spawn_thread(self):
        hub.spawn(self._start_monitor)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self._add_flow(datapath, 0, match, actions)

    def _add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=instructions,
            )
        else:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=priority,
                match=match,
                instructions=instructions,
            )

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug('Packet truncated: only %s of %s bytes', ev.msg.msg_len, ev.msg.total_len)

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self._mac_to_port.setdefault(dpid, {})

        self._mac_to_port[dpid][src] = in_port

        if dst in self._mac_to_port[dpid]:
            out_port = self._mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD and eth.ethertype == ether_types.ETH_TYPE_IP:
            ip = pkt.get_protocol(ipv4.ipv4)
            srcip = ip.src
            dstip = ip.dst

            match = parser.OFPMatch(
                in_port=in_port,
                eth_dst=dst,
                eth_src=src,
                eth_type=ether_types.ETH_TYPE_IP,
                ipv4_src=srcip,
                ipv4_dst=dstip
            )

            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self._add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self._add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )

        datapath.send_msg(out)

    def _start_monitor(self):
        while True:
            for datapath in self._datapaths.values():
                self._request_statistics_first(datapath)
            hub.sleep(3)

    def _request_statistics(self, datapath):
        self.logger.debug('Send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        self.logger.info('\n\n\n+--------------------+--------------+---------------------+-----------+')
        self.logger.info('|  ethernet address  |  ip address  |  number of packets  |  Blocked  |')
        self.logger.info('+--------------------+--------------+---------------------+-----------+')

        value = 0
        body = ev.msg.body
        for stat in sorted(
                [flow for flow in body if flow.priority == 1], key=lambda flow: (
                        flow.match['in_port'],
                        flow.match['eth_dst'],
                        flow.match['ipv4_src'],
                        flow.match['ipv4_dst'],
                    )
                ):

            if stat.match['ipv4_src'] != self._server_ip and stat is not None:
                value += 1

                blocked = 'YES' if stat.match['ipv4_src'] in self._banned_ips else 'NO'
                self._diff[value] = (stat.packet_count - self._request[value])
                self._request[value] = stat.packet_count
                self.logger.info(
                    '   %17s     %8s             %i             %3s    ',
                    stat.match['eth_src'],
                    stat.match['ipv4_src'],
                    self._request[value]+1,
                    blocked,
                )

                calc = self._diff[value] / 3
                if calc > 40 and stat.match['ipv4_src'] not in self._banned_ips:
                    print('DDoS ATTACK DETECTED!')
                    print('Dropping packets coming from the following IP:')
                    print(stat.match['ipv4_src'])

                    self._banned_ips.append(stat.match['ipv4_src'])
                    msg = ev.msg
                    datapath = msg.datapath
                    parser = datapath.ofproto_parser

                    mat = parser.OFPMatch(
                        eth_type=ether_types.ETH_TYPE_IP,
                        ipv4_src=stat.match['ipv4_src'],
                        ipv4_dst='10.0.0.1'
                    )

                    self._add_flow(ev.msg.datapath, 100, mat, [])
