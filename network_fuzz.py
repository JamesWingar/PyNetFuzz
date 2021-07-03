#!/usr/bin/env python3

# import from src
from src.arguments import parse_args
from src.hosts import Host
from src.packetGenerator import packet_generator
from src.packet import PacketDetails
from src import const

def main():

     # get args
    args = parse_args()

    # Create host objects
    target, source = Host(args.target_ip, args.target_mac, args.target_port), \
        Host(args.source_ip, args.source_mac, args.source_port)

    # Get seed from args
    seed = args.seed

    # create PacketDetails object from args
    packet_details = PacketDetails({
        'int_protocol': args.int_protocol,
        'trans_protocol': args.trans_protocol,
        'cast': args.cast,
        'headers': args.headers,
        'vlan': args.vlan,
        'min_length': args.min_length,
        'max_length': args.max_length,
    })

    # Packet count
    packet_count = 0

    while(packet_count < args.n_packets):

        # Test hosts (online)
        if not target.is_online():
            #report offline
            pass

        for packet in packet_generator(target, packet_details, source, seed):

            # send new packet
            packet.send(args.network_interface)

            # Log packet
            #TODO

            if packet_count < args.n_packets:
                break

        # confirm target is online
        if not target.is_online():
            #report offline
            pass

    # Output results
    #TODO

if __name__ == "__main__":
    main()