from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.arp import arp

log = core.getLogger()

# Load whitelist
whitelist = []

with open("/home/userrp/sdn_access_control/whitelist.txt", "r") as file:
    for line in file:
        src, dst = line.strip().split(",")
        whitelist.append((src, dst))


def _handle_PacketIn(event):
    packet = event.parsed
    connection = event.connection

    src = str(packet.src)
    dst = str(packet.dst)

    # Allow ARP packets (important)
    if packet.find('arp'):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        connection.send(msg)

        log.info("ARP Allowed")
        return

    log.info("Packet received: %s -> %s", src, dst)

    # Check whitelist
    if (src, dst) in whitelist:

        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst

        msg.actions.append(
            of.ofp_action_output(port=of.OFPP_FLOOD)
        )

        connection.send(msg)

        log.info("Allowed: %s -> %s", src, dst)

    else:

        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst

        # No action = DROP
        connection.send(msg)

        log.info("Blocked: %s -> %s", src, dst)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("SDN Access Control Controller Started")