"""
Contains Generator function - packet generator
"""
#Python library imports
import logging
# Package imports
from .randomiser import Randomiser
from .packet import Packet, PacketDetails
from .hosts import Host
from .const import PACKETS_PER_SEED
from .validation import valid_packet_details


def packet_generator(target: Host, details: PacketDetails,
        source: Host=None, seed: int=None, max_packets: int=PACKETS_PER_SEED) -> Packet:
    """ Generator method to create randomised packets

    Parameters:
        target (Host): Host object containing information for packet generation
        details (PacketDetails): Object contains required details for packet generation
        source (Host): Optional Host object for packet generation
        seed (int): Value for Randomiser to create Suedo-random numbers
        max_packets (int): Value for max packets to be created from a single generator

    Returns:
        Packet: Yields a created randomised packet
    """
    source =  source if source is not None else Host(None, None, None)
    details = valid_packet_details(details)
    randomiser = Randomiser(seed)
    logging.info("Packet generator seed: %s", randomiser.seed)

    random_target = Host(None, None, None)
    random_source = Host(None, None, None)
    random_details = PacketDetails({
        'trans_protocol': None,
        'cast': None,
        'int_protocol': None,
        'vlan': None,
        'headers': None})

    for _ in range(max_packets):
        # randomise hosts
        random_target = randomiser.host(target, random_target)
        random_source = randomiser.host(source, random_source)
        # randomise packet info
        random_details = randomiser.packet_details(details, random_details)

        # create packet
        packet = Packet(random_target, random_source, random_details)
        packet.add_all_layers()

        logging.debug("Generator Packet #%s: %s", _, packet)

        yield packet
