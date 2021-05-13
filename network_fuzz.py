#!/usr/bin/env python3

# import from src
from src.arguments import parse_args
from src.hosts import Host
from src.packet import PacketGenerator

def main():

     # get args
    args = parse_args()

    print(args)

    # Create host objects
    target, source = Host(args['target_ip'], args['target_mac'], args['target_port']), \
        Host(args['source_ip'], args['source_mac'], args['source_port'])

    print(target)
    print(source)

    # Test hosts (online)

    # Create packet generator object
    packet_generator = PacketGenerator(args)

    # Create 
    for number in range(1):
        # create new packet
        packet = packet_generator.create_packet(target, source)

        # send new packet

        # Log output

        # confirm target is online

    # Output results

if __name__ == "__main__":
    main()