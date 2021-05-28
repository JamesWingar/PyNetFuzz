from scapy.all import sr1, IP, ICMP, arping

class Host():
    
    def __init__(self, ip: str, mac: str, port: str) -> None:
        """ Host class built-in initialiser
   
        Parameters:
        ip (str): IP address string
        mac (str): MAC address string
        port (str): Port value string
    
        Returns:
        str: Randomised IP address string
        """
        self.ip = ip
        self.mac = self.get_MAC() if mac == 'self' else mac
        self.port = port
        self.online = False

    def is_online(self) -> bool:
        """ Checks if host is online
    
        Returns:
        bool: Returns true if host is online
        """
        self.online = self.ping_host()
        return self.online

    def is_ip(self):
        """ Checks if IP is present

        Returns:
        bool: Returns true if IP is present
        """
        return self.ip != None

    def is_mac(self):
        """ Checks if MAC is present

        Returns:
        bool: Returns true if MAC is present
        """
        return self.mac != None

    def is_port(self):
        """ Checks if Port is present

        Returns:
        bool: Returns true if Port is present
        """
        return self.port != None

    def ping_host(self) -> bool:
        """ Pings host IP

        Returns:
        bool: Returns true if ping is successful
        """
        if not self.is_ip():
            raise ValueError("Can not ping a host with no IP address.")

        return sr1(
            IP(dst=self.ip) / ICMP(),
            timeout=1,
            verbose=False
        ) is not None

    def get_MAC(self) -> str:
        """ Gets host MAC address by ARPing host IP address

        Returns:
        str: Returns MAC address string if ARPing is successful
        """
        if not self.is_ip():
            raise ValueError("Can not get MAC address of a host without an IP address.")
        
        ans, unans = arping(self.ip, verbose=False)
        for (sent, receive) in ans:
            if receive.psrc == self.ip:
                return receive.src
        return None

    def __str__(self) -> str:
        return f"IP: {self.ip}\nMAC: {self.mac}\nPort: {self.port}\nOnline: {self.online}"
