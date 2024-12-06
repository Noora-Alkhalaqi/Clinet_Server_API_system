import socket
import threading
import requests
import pickle
import json
import sys

# my API key
API_KEY = "5d0fd747e02946bb8f1db8e5558ba8a5"

# Global variables
global server_socket
global running

def handle_client_connection(client_socket, client_name):
    try:
        print(f"{client_name} connected.")
        while True:
            # Receive the request from the client
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                print(f"No request received from {client_name}. Closing connection.")
                break

            # Handle "Quit" request
            if request == "Quit":
                print(f"Disconnected from {client_name}")
                break

            # Parse the request
            request_parts = request.split('-')
            if len(request_parts) < 2 or len(request_parts) > 3:
                client_socket.sendall(pickle.dumps(["Invalid request format."]))
                continue

            request_type = request_parts[0]  # 1 for headlines, 2 for sources
            option = request_parts[1]       
            key = request_parts[2] if len(request_parts) == 3 else ''  # Optional key
            group_id = "A16"  # group ID

            # Process the request
            if request_type == '1':  # Headlines
                query = get_headlines_query(option, key)
                url = f"https://newsapi.org/v2/top-headlines?{query}&apiKey={API_KEY}"
                print(f"Fetching headlines from URL: {url}")
                data_list = fetch_data(url, "articles", client_name)

            elif request_type == '2':  # Sources
                query = get_sources_query(option, key)
                url = f"https://newsapi.org/v2/sources?{query}&apiKey={API_KEY}"
                print(f"Fetching sources from URL: {url}")
                data_list = fetch_data(url, "sources", client_name)

            else:
                data_list = ["Invalid request type."]

            # Send the data back to the client
            client_socket.sendall(pickle.dumps(data_list))

            # Save the data to a JSON file
            write_to_json(data_list, client_name, request_type ,option, group_id)

    except Exception as e:
        print(f"Error handling client {client_name}: {e}")
    finally:
        client_socket.close()

def write_to_json(data_list, client_name, request_type , option, group_id):
    """Save the data to a JSON file."""
    json_file_name = f"{client_name}_{request_type}_{option}_{group_id}.json"
    with open(json_file_name, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)
    print(f"Data written to {json_file_name}.")

def get_headlines_query(option, key):
    """Construct the query for fetching headlines."""
    if option == '1':  # Search by keyword
        return f"q={key}"
    elif option == '2':  # Search by category
        return f"category={key}"
    elif option == '3':  # Search by country
        return f"country={key}"
    elif option == '4':  # List all headlines
        return "country=us"  # Default to US headlines
    return ""

def get_sources_query(option, key):
    """Construct the query for fetching sources."""
    if option == '1':  # Search by category
        return f"category={key}"
    elif option == '2':  # Search by country
        return f"country={key}"
    elif option == '3':  # Search by language
        return f"language={key}"
    elif option == '4':  # List all sources
        return ""  # No additional parameters needed
    return ""

def fetch_data(url, data_key, client_name):
    """Fetch data from the NewsAPI."""
    data_list = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"Request successful from {client_name}")
        file_contents = response.json()

        if data_key in file_contents and len(file_contents[data_key]) > 0:
            for count, item in enumerate(file_contents[data_key][:15], start=1):
                entry = parse_item(item, data_key, count)
                data_list.append(entry)
        else:
            data_list.append(["No data found."])
    except requests.exceptions.HTTPError as http_err:
        data_list.append([f"HTTP error occurred: {http_err}"])
    except requests.exceptions.RequestException as req_err:
        data_list.append([f"Request error occurred: {req_err}"])
    except Exception as e:
        data_list.append([f"Unexpected error: {e}"])
    return data_list

def parse_item(item, data_key, count):
    """Parse an item from the API response."""
    if data_key == "articles":
        return {
            "id": count,
            "source": item['source']['name'],
            "author": item.get('author', 'N/A'),
            "title": item['title'],
            "url": item['url'],
            "description": item.get('description', 'No description available.'),
            "publishedAt": item['publishedAt']
        }
    elif data_key == "sources":
        return {
            "id": count,
            "name": item['name'],
            "description": item['description'],
            "url": item['url'],
            "category": item['category'],
            "language": item['language'],
            "country": item['country']
        }

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
    """Main server function."""
    global server_socket
    global running
    running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(5)
    print("Server is listening for connections...")

    # Start the keyboard input thread
    keyboard_thread = threading.Thread(target=keyboard_input_thread)
    keyboard_thread.start()

    try:
        while running:
            client_socket, client_address = server_socket.accept()
            client_name = client_socket.recv(1024).decode('utf-8')
            print(f"Connected to {client_name} at {client_address}.")
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_socket, client_name),
                daemon=True
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        running = False
        server_socket.close()

if __name__ == "__main__":
    main()