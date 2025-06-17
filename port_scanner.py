import socket
import argparse
from datetime import datetime
import threading

open_ports = []
lock = threading.Lock()

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                with lock:
                    open_ports.append(port)
                    print(f"[OPEN] Port {port}")
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Simple Multithreaded Port Scanner")
    parser.add_argument("target", help="Target IP or domain to scan")
    parser.add_argument("-p1", "--start-port", type=int, default=1, help="Start of port range")
    parser.add_argument("-p2", "--end-port", type=int, default=1024, help="End of port range")
    parser.add_argument("-o", "--output", help="Save results to file (optional)")

    args = parser.parse_args()
    target = args.target
    start_port = args.start_port
    end_port = args.end_port

    print(f"\n[+] Scanning {target} from port {start_port} to {end_port}...")
    print(f"Started at: {datetime.now()}\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nFinished at: {datetime.now()}")

    if args.output:
        with open(args.output, 'w') as f:
            for port in open_ports:
                f.write(f"Port {port} is OPEN\n")
        print(f"\n[+] Results saved to {args.output}")

if __name__ == "__main__":
    main()
