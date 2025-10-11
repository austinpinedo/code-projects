#simple network scanner 
import socket, ipaddress

def scan(ip, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"{ip}:{port} OPEN")
        sock.close()

    except:
        pass

network_ip = ipaddress.ip_network(input("enter an ip address:"))

for ip in network_ip.hosts():
    for port in range(1, 1024):
        scan(str(ip), port)