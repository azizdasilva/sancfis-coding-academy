from scapy.all import *
import argparse

TIME_OUT = 2


def arp_ping(subnet): # Function for discovering and probing hosts on a computer network.
    """ARP Pings entire subnet returns found in subnet."""
    conf.verb = 0
    answered, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet), timeout=TIME_OUT, verbose=False, inter=0.1)
    return [rcv.sprintf(r"%Ether.src% - %ARP.psrc%") for snd, rcv in answered]


def tcp_scan(dst_ip, stealth=False): # Function for building the systems and users ports known. An then scans TCP ports for availability
    """Scans TCP ports for availability."""

    system_ports = {20: 'FTP', # Set data structure for collection which is unordered and unindexed for system ports
                    21: 'FTP Control',
                    22: 'SSH',
                    23: 'Telnet',
                    25: 'SMPT',
                    53: 'DNS',
                    67: 'DHCP Server',
                    68: 'DHCP Client',
                    69: 'TFTP',
                    80: 'HTTP',
                    110: 'POP3',
                    119: 'NNTP',
                    139: 'NetBIOS',
                    143: 'IMAP',
                    389: 'LDAP',
                    443: 'HTTPS',
                    445: 'SMB',
                    465: 'SMTP',
                    569: 'MSN',
                    587: 'SMTP',
                    990: 'FTPS',
                    993: 'IMAP',
                    995: 'POP3'}

    user_ports = {1080: 'SOCKS', # Set data structure for collection which is unordered and unindexed for user ports
                  1194: 'OpenVPN',
                  3306: 'MySQL',
                  3389: 'RDP',
                  3689: 'DAAP',
                  5432: 'PostGreSQL',
                  5800: 'VNC',
                  5900: 'VNC',
                  6346: 'Grutella',
                  8080: 'HTTP'}

    def tcp_default(dst_port, src_port): # Function for a simple tcp scan 
        """Default TCP Scan."""
        default_scan = sr1(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=TIME_OUT) 
        if default_scan is not None:
            if(default_scan.getlayer(TCP).flags == 0x12): #  If the response flags value is 0x12 we have a SYN/ACK. The port is open. We send back a RST packet so we do not establish a connection.
                send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="AR"), timeout=TIME_OUT) # Close the connection by sending a RST
                return "Open"
        return "Closed"

    def tcp_stealth(dst_port, src_port): # Function for a stealth scan by remaining undetected
        """Stealthy TCP Scan"""
        stealth_scan = sr1(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=TIME_OUT)
        if stealth_scan is not None:
            if stealth_scan.getlayer(TCP).flags == 0x12: # If the response flags value is 0x12 we have a SYN/ACK. The port is open. We send back a RST packet so we do not establish a connection.
                send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="R"), timeout=TIME_OUT) # Close the connection by sending a RST
                return "Open"
            elif stealth_scan.getlayer(TCP).flags == 0x14: #  If the response flags value is 0x14 we have a SYN/RST.
                return "Closed"
        return "Filtered"

    def log_ports(ports, stealth=False): # Function for logging all port status
        """Logs status and info of ports."""
        log_ports = []

        for dst_port, nme_port in ports.iteritems(): # Go throught the log ports 
            src_port = RandShort()
            if default:
                stat = tcp_default(dst_port, src_port)
                log_ports.append('[*] TCP default scan: dest_ip=%s port=%d, service=%s, status=%s' % (dst_ip, dst_port, nme_port, stat))
            else:
                stat = tcp_stealth(dst_port, src_port)
                log_ports.append('[*] TCP stealth scan: dest_ip=%s port=%d, service=%s, status=%s' % (dst_ip, dst_port, nme_port, stat))

        return log_ports

    ports = []
    ports += ['[!] User Ports']
    ports += log_ports(user_ports, stealth)

    ports += ['[!] System Ports']
    ports += log_ports(system_ports, stealth)

    return ports


def parse_arguments(): # Function for parsing arguments to clean the command line input such as space etc...
    """Arguments parser."""
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <subnet>',
                                     description='port scanning tool @Ludisposed',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python port_scan.py "192.168.1.0/24" -s
python port_scan.py "192.168.1.0/24" --timeout 10
''')
    parser.add_argument('-s', '--stealth', default=False, action="store_true", help='Stealthy TCP scan')
    parser.add_argument('--timeout', type=int, help='Timeout parameter of scans')

    if args.timeout is not None:
        global TIME_OUT
        TIME_OUT = args.timeout

    return parser.parse_args()

if __name__ == '__main__': # Execution 
    args = argparse.ArgumentsParser()

    conf.verb = 0
    network = arp_ping(args.subnet)
    for connection in network:
        mac, ip = connection.split(' - ')
        print '\n\n[!] Trying port scan of current connection with mac=%s and ip=%s' % (mac, ip)
        for result in tcp_scan(ip, args.stealth):
            print result