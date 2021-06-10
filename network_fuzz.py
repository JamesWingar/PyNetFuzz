#!/usr/bin/env python3

# import from src
from src.arguments import parse_args
from src.hosts import Host
from src.packetGenerator import PacketGenerator
from src import const

def main():

     # get args
    args = parse_args()

    # Create host objects
    target, source = Host(args.target_ip, args.target_mac, args.target_port), \
        Host(args.source_ip, args.source_mac, args.source_port)

    while(PacketGenerator.count < args.n_packets):
        # Create packet generator object
        packet_generator = PacketGenerator(vars(args))

        # Test hosts (online)
        if not target.is_online():
            #report offline
            pass

        for number in range(const.PACKETS_PER_SEED):
            # create new packet
            packet = packet_generator.create_packet(target, source)

            # send new packet
            packet.send(args.network_interface)

            # Log packet
            #TODO

        # confirm target is online
        if not target.is_online():
            #report offline
            pass

    # Output results
    #TODO

if __name__ == "__main__":
    main()