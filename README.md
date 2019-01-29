Packet Differential Encoding
============================

Send data between hosts on a network without sending a single byte in the packet
itself.

This method uses the time between packets to encode data. Read the [blog
post][blog_post] for more information.

Installation
------------

`pip3 install git+https://github.com/vimist/packet_differential_encoding`

### Dependencies

 * `python3` (tested in Python 3.7.2)
 * `scapy` (automatically installed with the above command)
 * `tcpdump` (scapy requires this for certain operations)

Please check the [scapy installation][scapy_installation] instructions for more
details.

Sending Data
------------

`diff-packets send <interface> <host> <message>`

If you get errors running this, you'll probably need to run it as root using
`sudo`. It is however possible to configure your system to run this as non-root
if required.

Receiving Data
--------------

`diff-packets receive`

If you get errors running this, you'll probably need to run it as root using
`sudo`. It is however possible to configure your system to run this as non-root
if required.


[blog_post]: https://vimist.github.io/2019/01/30/Steganographic-Packets.html
[scapy_installation]: https://scapy.readthedocs.io/en/latest/installation.html
