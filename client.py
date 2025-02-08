import socket
import hashlib
import os

HOST = '127.0.0.1'  # Server address
PORT = 5000  # Port number
CHUNK_SIZE = 1024  # 1KB per chunk

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def send_file(file_path, client_socket):
    """Send a file to the server."""
    file_name = os.path.basename(file_path)

    # Send filename
    client_socket.send(file_name.encode())
    
    # Wait for ACK
    ack = client_socket.recv(10).decode()
    if ack != "ACK":
        print("[!] Server did not acknowledge filename. Aborting.")
        return None
    
    print(f"[*] Sending file: {file_name}")

    # Send file data
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            client_socket.send(chunk)

    client_socket.shutdown(socket.SHUT_WR)  # Let server know file transfer is done

    # Receive checksum from server
    received_checksum = client_socket.recv(64).decode()
    print(f"[*] Received checksum from server: {received_checksum}")
    return received_checksum

def main():
    while True:
        file_path = input("Enter the file path to send (or type 'exit' to quit): ").strip()
        if file_path.lower() == 'exit':
            print("[!] Exiting...")
            break
        
        if not os.path.exists(file_path):
            print("[!] File does not exist! Try again...")
            continue
        
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            
            received_checksum = send_file(file_path, client_socket)
            if not received_checksum:
                print("[!] File transfer failed. Try again...")
                continue
            
            computed_checksum = calculate_checksum(file_path)
            print(f"[*] Computed checksum: {computed_checksum}")
            
            if received_checksum == computed_checksum:
                print("✅ Transfer Successful")
            else:
                print("❌ Transfer Failed: Checksum mismatch")
        
        except Exception as e:
            print(f"[!] Error: {e}")
        
        finally:
            client_socket.close()
            print("\n[+] Ready for next file transfer...\n")

if __name__ == "__main__":
    main()
