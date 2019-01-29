import argparse
import sys

from packet_differential_encoding import Encoder, Decoder


def send(interface, message, host):
    with Encoder(interface) as encoder:
        encoder.send_data(bytes(message, 'UTF-8'), host)


def receive():
    decoder = Decoder()
    decoder.register_callback(
        lambda d: print(chr(d[-1]), end='', flush=True))
    decoder.listen()


def main(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='direction')

    send_parser = subparsers.add_parser('send')
    send_parser.add_argument(
        'interface', help='The interface to send the ICMP packets from')
    send_parser.add_argument('host', help='The host to send the ICMP packets to.')
    send_parser.add_argument('message', help='The message to send.')

    receive_parser = subparsers.add_parser('receive')

    args = parser.parse_args(argv)

    if args.direction == 'send':
        send(args.interface, args.message, args.host)
    elif args.direction == 'receive':
        receive()
    else:
        parser.error('\'send\' or \'receive\' required as first argument')

def main_cli_args():
    main(sys.argv[1:])

if __name__ == '__main__':
    main_cli_args()
