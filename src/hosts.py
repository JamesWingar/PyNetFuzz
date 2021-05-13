from scapy.all import sr1, IP, ICMP, arping

class Host():
    # Initialising
    def __init__(self, ip: str, mac: str, port: str) -> None:
        self.ip = ip
        self.mac = self.get_MAC(self.ip) if mac == 'self' else mac
        self.port = port
        self.online = False

    # Methods
    def is_online(self):
        self.online = self.ping_host()
        return self.online

    def is_ip(self):
        return self.ip != None

    def is_mac(self):
        return self.mac != None

    def is_port(self):
        return self.port != None

    def ping_host(self) -> bool:
        ping_packet = IP(dst=self.ip) / ICMP()
        return sr1(ping_packet, timeout=1, verbose=False) is not None

    def get_MAC(self) -> str:
        ans, unans = arping(self.ip, verbose=False)
        for (sent, receive) in ans:
            if receive.psrc == self.ip:
                return receive.src
        return None

    def __str__(self):
        return f"IP: {self.ip}\nMAC: {self.mac}\nPort: {self.port}\nOnline: {self.online}\n"
