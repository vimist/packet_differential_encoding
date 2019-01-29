from time import sleep

from scapy.all import IP, ICMP, conf, sniff


INTERVALS = list(range(10, 170, 10))
"""The 16 intervals used to encode our nibbles."""


class Encoder:
    """Encode and send data using the time between ICMP packets."""

    def __init__(self, interface):
        self._interface = interface
        self._socket = None

    def __enter__(self):
        self._socket = conf.L3socket(
            iface=self._interface)

        return self

    def __exit__(self, *args):
        self._socket.close()

    def _ping(self, host):
        packet = IP(dst=host)/ICMP()
        self._socket.send(packet)

    def send_data(self, data, host):
        """Send data to the given host."""
        self._ping(host)

        for byte in data:
            un = byte >> 4
            ln = byte & 0b1111

            sleep(INTERVALS[un]/1000)
            self._ping(host)

            sleep(INTERVALS[ln]/1000)
            self._ping(host)


class Decoder:
    """Receive and decode data encoded using the time between ICMP packets."""
    def __init__(self):
        self._last_packet_time = None

        self.packets_received = 0
        self._current_byte = 0
        self.data = b''

        self._callbacks = []

    def register_callback(self, callback):
        """Register a function to be called when new data is received."""
        self._callbacks.append(callback)

    def _call_callbacks(self, data):
        for callback in self._callbacks:
            callback(data)

    def _process(self, packet):
        self.packets_received += 1

        if self.packets_received > 1:
            packet_delta = (packet.time - self._last_packet_time) * 1000

            # Reset the connection if we haven't received a packet for a while
            if packet_delta > INTERVALS[-1]*3:
                self.packets_received = 1
                self._current_byte = 0

            # Calculate the closest interval
            best_fit = (0, float('inf'))
            for interval in INTERVALS:
                error = abs(packet_delta - interval)

                if error < best_fit[1]:
                    best_fit = (interval, error)

            value = INTERVALS.index(best_fit[0])

            # Add the nibble to the current byte
            self._current_byte = (self._current_byte << 4) | value

            # If we have a full byte of data
            if self.packets_received % 2 == 1:
                self.data += bytes([self._current_byte])
                self._call_callbacks(self.data)
                self._current_byte = 0

        self._last_packet_time = packet.time

    def listen(self):
        """Start listening for ICMP packets."""
        sniff(filter='icmp[icmptype] = 8', prn=self._process)
