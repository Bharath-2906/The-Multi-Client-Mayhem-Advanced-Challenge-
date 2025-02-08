import socket
import threading
import hashlib
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000  # Port number
CHUNK_SIZE = 1024  # 1KB per chunk

os.makedirs("files", exist_ok=True)

def calculate_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def handle_client(client_socket, address):
    print(f"[+] Connection established: {address}")

    # Receive and validate filename
    file_name = client_socket.recv(1024).decode().strip()
    print(f"[*] Received filename: '{file_name}'")  # Debugging log
    
    if not file_name or any(char in file_name for char in r'\/:*?"<>|'):
        print("[!] Invalid filename received")
        client_socket.close()
        return
    
    client_socket.send("ACK".encode())  # Send acknowledgment to the client
    
    file_path = os.path.join("files", os.path.basename(file_name))
    
    # Receive file content
    with open(file_path, 'wb') as f:
        while True:
            chunk = client_socket.recv(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
    
    print(f"[*] File '{file_name}' received successfully.")

    # Compute checksum
    checksum = calculate_checksum(file_path)
    print(f"[*] Calculated checksum: {checksum}")
    client_socket.send(checksum.encode())

    client_socket.close()
    print(f"[-] Connection closed: {address}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    main()
import socket
import threading
import hashlib
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000  # Port number
CHUNK_SIZE = 1024  # 1KB per chunk

os.makedirs("files", exist_ok=True)

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def handle_client(client_socket, address):
    print(f"[+] Connection established: {address}")

    # Receive and validate filename
    file_name = client_socket.recv(1024).decode().strip()
    print(f"[*] Received filename: '{file_name}'")  

    if not file_name or any(char in file_name for char in r'\/:*?"<>|'):
        print("[!] Invalid filename received")
        client_socket.close()
        return
    
    client_socket.send("ACK".encode())  # Send acknowledgment to the client

    file_path = os.path.join("files", os.path.basename(file_name))
    
    # Receive file content
    with open(file_path, 'wb') as f:
        while True:
            chunk = client_socket.recv(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)

    print(f"[*] File '{file_name}' received successfully.")

    # Compute checksum
    checksum = calculate_checksum(file_path)
    print(f"[*] Calculated checksum: {checksum}")
    client_socket.send(checksum.encode())  # Send checksum to client

    client_socket.close()
    print(f"[-] Connection closed: {address}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    main()
