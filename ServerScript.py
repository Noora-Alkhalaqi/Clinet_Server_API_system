import socket
import threading
import json

API-Key = "5d0fd747e02946bb8f1db8e5558ba8a5"

def start_server(host='localhost', port=65432):
    """
    Creates a TCP server socket, binds it to the given host and port,
    and starts listening for incoming connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Listen up to 5 connections
    print(f"Server is listening on {host}:{port}")
    return server_socket

# Handle individual client connections
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        # Receive and store client's username
        username = client_socket.recv(1024).decode('utf-8')
        print(f"Client connected: {username} ({client_address})")

        while True:
            # Receive the user's main menu selection
            message = client_socket.recv(1024).decode('utf-8')
            if not message:  # Client disconnected
                break

            print(f"Request from {username}: {message}")
            if message == "1":  # Client chose to search headlines
                send_headlines_menu(client_socket, username)
            elif message == "2":  # Client chose to search sources
                send_sources_menu(client_socket, username)
            elif message == "3":  # Client chose to quit
                print(f"Client {username} disconnected.")
                break
            else:
                client_socket.sendall("Invalid option. Please try again.".encode('utf-8'))

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Client disconnected: {username} ({client_address})")

# Handle headlines menu
def send_headlines_menu(client_socket, username):
    """
    Handles the Search Headlines menu and processes the client's choices.
    """
   
# Handle sources menu interaction
def send_sources_menu(client_socket, username):
    """
    Handles the List of Sources menu and processes the client's choices.
    """
    

