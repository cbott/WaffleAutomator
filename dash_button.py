# Note: requires root
import threading

from scapy.all import ARP, sniff

NETWORK_REQUEST = 1

class AmazonDashButton:
    """
    Utility class for polling a network and triggering an action when an
    Amazon Dash Button is pressed
    """
    def __init__(self, mac_addresses, callback):
        """
        mac_addresses [List]: MAC addresses of the buttons that will be registered
        callback [Callable]: the function to run when a button is pressed
        """
        self.macs = mac_addresses
        self.callback = callback

        polling_thread = threading.Thread(target=self._poll)
        polling_thread.start()

    def _poll(self):
        """ Watch the network for ARP broadcast events """
        sniff(prn=self._handler, filter="arp", store=0)

    def _handler(self, packet):
        """ Handle ARP broadcast events """
        message_type = packet[ARP].op
        mac_address = packet[ARP].hwsrc
        if message_type == NETWORK_REQUEST and mac_address in self.macs:
            self.callback()
    # TODO: stop/start methods perhaps
