import os
import socket
import sys
import ipaddress
import time
import threading

import ip_header_struct
import ip_header_ctypes
import icmp_header_struct

SUBNET = '192.168.1.0/24'
MESSAGE = 'PYTHONRULES'

def udp_sender(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), port))

class Scanner:
    def __init__(self, host):
        self.host = host

        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f'{str(self.host)}'])
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = ip_header_ctypes.IPC(raw_buffer[0:20])

                if ip_header.protocol == 'ICMP':
                    # print(
                    #         'Protocol: %s %s -> %s' % (ip_header.protocol,
                    #             ip_header.src_address, 
                    #             ip_header.dst_address)
                    #         )

                    offset = ip_header.ihl * 4
                    icmp_buff = raw_buffer[offset:offset+8]

                    icmp_header = icmp_header_struct.ICMP(icmp_buff)

                    if (icmp_header.code == 3 and icmp_header.type == 3 and
                            ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET) and
                            raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8') and
                            str(ip_header.src_address) not in hosts_up
                            ):
                                tgt = str(ip_header.src_address)
                                hosts_up.add(tgt)
                                
                                print(f'Host UP: {tgt}')

        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\n User interrupted.')

            if hosts_up:
                print(f'\n\nSummary: Hosts up on {SUBNET}')

            for host in sorted(hosts_up):
                print(f'{host}')

            print('')

            sys.exit()

if __name__ == '__main__':

    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.110'

    s = Scanner(host)
    time.sleep(5)

    ports = [123, 129, 139, 22, 53, 56129, 53152, 2345, 123, 999, 80, 1520, 12345, 1234]
    for port in ports:
        t = threading.Thread(target=udp_sender, args=(port,))
        t.start()

    s.sniff()

