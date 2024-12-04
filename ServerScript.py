import socket
import threading
import requests
import pickle
import json
import sys

API_KEY = "5d0fd747e02946bb8f1db8e5558ba8a5"
global server_socket
global running


def handle_client_connection(client_socket, client_name):
    try:
        print(f"{client_name} connected.")
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                print(f"No request received from {client_name}. Closing connection.")
                break
            
            if request == "Quit":
                print(f"Disconnected from {client_name}")
                break
            
            request_parts = request.split('-')
            if len(request_parts) != 3:
                print(f"Invalid request format from {client_name}: {request}")
                continue  # Skip to the next iteration

            request_type, option, key = request_parts
            data_list = []

            if option == '1':
                url = f"https://newsapi.org/v2/top-headlines?{get_headlines_query(request_type, key)}&apiKey={API_KEY}"
                print(f"Fetching data from URL: {url}")
                data_list = fetch_data(url, "articles", client_name)

            elif option == '2':
                url = f"https://newsapi.org/v2/top-headlines/sources?{get_sources_query(request_type, key)}&apiKey={API_KEY}"
                print(f"Fetching data from URL: {url}")
                data_list = fetch_data(url, "sources", client_name)

            # Save data to JSON file
            group_id = "A16"  # Replace with actual group ID logic if needed
            json_file_name = f"{client_name}_{option}_{group_id}.json"
            with open(json_file_name, 'w') as json_file:
                json.dump(data_list, json_file, indent=4)
                print(f"Data saved to {json_file_name}")

            # Send serialized response back to client
            serialized_list = pickle.dumps(data_list)
            client_socket.sendall(serialized_list)

            # Allow the client to select a specific item
            if data_list:
                client_socket.sendall(pickle.dumps(["Select an item by number:"]))
                selected_item_data = client_socket.recv(4096)
                selected_index = pickle.loads(selected_item_data)[0]  # Assuming client sends the index
                if 0 <= selected_index < len(data_list):
                    # Send detailed information about the selected item
                    detailed_info = data_list[selected_index]
                    client_socket.sendall(pickle.dumps(detailed_info))
                else:
                    client_socket.sendall(pickle.dumps(["Invalid selection."]))
    except Exception as e:
        print(f"Error handling client {client_name}: {e}")
    finally:
        client_socket.close()  # Ensure the socket is closed regardless of errors

def get_headlines_query(request_type, key):
    if request_type == '1':  # Keyword search
        return f"q={key}"
    elif request_type == '2':  # Category search
        return f"category={key}"
    elif request_type == '3':  # Country search
        return f"country={key}"
    else:
        return "country=us"  # Default to US headlines

def get_sources_query(request_type, key):
    if request_type == '1':  # Category search
        return f"category={key}"
    elif request_type == '2':  # Country search
        return f"country={key}"
    elif request_type == '3':  # Language search
        return f"language={key}"
    else:
        return ""  # All sources

def fetch_data(url, data_key, client_name):
    data_list = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Request successful from {client_name}")
        file_contents = response.json()

        if data_key in file_contents and len(file_contents[data_key]) > 0:
            for count, item in enumerate(file_contents[data_key][:15], start=1):
                entry = parse_item(item, data_key, count)
                data_list.append(entry)
        else:
            data_list.append(["No news found or server is not reachable."])
    except requests.exceptions.HTTPError as http_err:
        data_list.append([f"HTTP error occurred: {http_err}"])
        print(f"HTTP error for client {client_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        data_list.append([f"Request error occurred: {req_err}"])
        print(f"Request error for client {client_name}: {req_err}")

    return data_list

def parse_item(item, data_key, count):
    if data_key == "articles":
        return [
            f"({count})", 
            f"name: {item['source']['name']}",
            f"author: {item['author']}",
            f"title: {item['title']}",
            f"url: {item['url']}",
            f"description: {item['description']}",
            f"publish date: {item['publishedAt']}"
        ]
    else:  # sources
        return [
            f"({count})", 
            f"name: {item['name']}",
            f"description: {item['description']}",
            f"url: {item['url']}",
            f"category: {item['category']}",
            f"language: {item['language']}",
            f"country: {item['country']}"
        ]
    

# Method to allow an input (ctrl + C) to shutdown server 
def keyboard_input_thread():
    global running
    while running:
        try:
            input()  # Wait for user input
        except EOFError:
            print("Server shutting down...")
            running = False  
            server_socket.close()
            sys.exit()    

def main():
    global server_socket
    global running
    running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(3)
    print("Server is listening for connections...")

    # Create a thread for keyboard input handling
    keyboard_thread = threading.Thread(target=keyboard_input_thread)
    keyboard_thread.start()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_name = client_socket.recv(1024).decode('utf-8')
            print(f"Connected to {client_name} at {client_address}.")
            client_handler = threading.Thread(target=handle_client_connection, args=(client_socket, client_name), daemon=True)
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        running = False
        server_socket.close()

if __name__ == "__main__":
    main()