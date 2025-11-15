#simple network scanner 
import socket, argparse, json

def scan_port(ip: str, port: int, timeout: float) -> bool:

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"{ip}:{port} OPEN")
        sock.close()

    except:
        pass

def scan_host(host: str, start_port: int, end_port: int, timeout: float) -> bool:
    pass
            
def main():
    parser = argparse.ArgumentParser(description="tcp port scanner")
    parser.add_argument("--host", required=True, help="target IP")
    parser.add_argument("--start-port", type=int, default=1, help="starting port range (default: 1)")
    parser.add_argument("--end-port", type=int, default=1024, help="ending port range (default: 1024)")
    args = parser.parse_args()
    
    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        raise ValueError("invalid port range") 

if __name__ == "__main__":
    main()