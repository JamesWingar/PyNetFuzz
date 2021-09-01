"""
Contains main run method and logging setup
"""
# Python library imports
import logging
import time
# Package imports
from .arguments import Args
from .hosts import Host
from .packet_generator import packet_generator
from .packet import PacketDetails
from .const import LOGGING_FORMAT, LOGGING_LEVEL


def run(args: Args) -> None:
    """ Main run method, setups up logging, generates and sends packets.
    Can be imported and run from a script or run via commandline (PyNetFuzz.py)

    Parameters:
        args (Args): An object containing all required arguments to run.
            Contains: target_ip, source_ip, network_interface, n_packets,
                target_mac, source_mac, target_port, source_port, int_protocol,
                trans_protocol, cast, headers, vlan, min_length , max_length, seed
    """
    configure_logging()
    logging.info("starting PyNetFuzzing...")
    target, source = Host(args.target_ip, args.target_mac, args.target_port), \
        Host(args.source_ip, args.source_mac, args.source_port)
    packet_details = PacketDetails({
        'int_protocol': args.int_protocol,
        'trans_protocol': args.trans_protocol,
        'cast': args.cast,
        'headers': args.headers,
        'vlan': args.vlan,
        'min_length': args.min_length,
        'max_length': args.max_length,
    })
    logging.info("Target(%s)", target)
    logging.info("Source(%s)", source)
    logging.info("PacketDetails(%s)", packet_details)

    packet_count, gen_count, start_time = 0, 0, time.time()
    while packet_count < args.n_packets:

        if not target.is_online():
            logging.error("Target is offline (%s)", target.ip)

        logging.info("Starting packet generator (Pkt=%s, Gen=%s)", packet_count, gen_count)
        for packet in packet_generator(target, packet_details, source, args.seed):
            packet.send(args.network_interface)
            packet_count += 1

            if packet_count >= args.n_packets:
                break

        gen_count += 1
        logging.info("Terminated packet generator (Pkt=%s, Gen=%s)", packet_count, gen_count)

        if not target.is_online():
            logging.error("Target is offline (%s)", target.ip)

    # Output results
    time_diff = time.time() - start_time
    message = f"[Completed] Sent: {packet_count}, Time: {time_diff}s"
    logging.info(message)
    print(message)

def configure_logging():
    """ Configure logging to default file"""
    logging.basicConfig(filename=f'logs/{int(time.time())}.log',
        format=LOGGING_FORMAT, level=logging.INFO)
    logger=logging.getLogger()
    logger.setLevel(LOGGING_LEVEL.upper())
