#Python library imports

# Package imports
from src.randomiser import Randomiser
from src.packet import Packet, PacketDetails
from src.hosts import Host
from src.const import (
    PACKETS_PER_SEED,
)
from src.validation import (
    valid_host,
    valid_packet_details,
)

def packet_generator(target: Host, details: PacketDetails, source: Host=Host(None, None, None), seed: int=None, max_packets: int=PACKETS_PER_SEED):
    """ Generator method to create randomised packets
   
        Parameters:
        target (Host): Host object containing information for packet generation
        packet_details (PacketDetails): Object contains required details for packet generation
        source (Host): Optional Host object for packet generation
        seed (int): Value for Randomiser to create Suedo-random numbers
        max_packets (int): Value for max packets to be created from a single generator

        Returns:
        Packet: Yields a created randomised packet 
    """
    target = valid_host(target)
    details = valid_packet_details(details)
    randomiser = Randomiser(seed)

    for _ in range(max_packets):     
        # randomise hosts   
        random_target = randomiser.host(target) 
        random_source = randomiser.host(source)
        # randomise packet info
        random_details = randomiser.packet_details(details, details.min_length, details.max_length) 

        # create packet
        packet = Packet(random_target, random_source, random_details)
        packet.add_all_layers()
        
        # output created packet
        print(f"Packet #{_}: {packet}")

        yield packet
