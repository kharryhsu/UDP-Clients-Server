import socket
import argparse
import threading

def handle_client(server_socket, data, client_address):
    try:
        print(f"Received from client {client_address}: {data.decode('utf-8')}\n")
        
        msg = f"Hey, Client {client_address[0]}"
        
        server_socket.sendto(msg.encode('utf-8'), client_address)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    

def start_server(addr='localhost', port=12345):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((addr, port))
        
        print(f'Server is listening on port {addr}:{port}...\n')
        
        while True:
            try:
                data, client_address = server_socket.recvfrom(1024)
                
                client_thread = threading.Thread(target=handle_client, args=(server_socket, data, client_address))
                client_thread.start()
            except Exception as e:
                print(f'Error receiving data: {e}')
    except Exception as e:
        print(f'Server error: {e}')
    finally:
        server_socket.close()
        print("Server shutdown.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="UDP Client")
    parser.add_argument('--addr', type=str, default='localhost', help="Server address (default: localhost)")
    parser.add_argument('--port', type=int, default=12345, help="Server port (default: 12345)")
    
    return parser.parse_args()

def configure_with_input():
    addr = input("Enter server address (default 'localhost'): ") or 'localhost'
    port = input("Enter server port (default 12345): ")
    port = int(port) if port else 12345
    
    return addr, port

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.addr == 'localhost' and args.port == 12345:
        addr, port = configure_with_input()
    else:
        addr, port = args.addr, args.port
    
    start_server(addr=addr, port=port)