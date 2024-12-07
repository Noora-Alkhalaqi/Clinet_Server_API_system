import socket
import pickle

def send_message(cs, message):
    ''' Sends the message to the server. '''
    try:
        cs.sendall(message.encode('utf-8'))
        print(f"Sent message: {message}")  
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(cs):
    """Receives a length-prefixed message from the server."""
    try:
        # Read the first 4 bytes to determine the message length
        raw_length = cs.recv(4)
        if not raw_length:
            print("No data received. Connection may have been closed.")
            return []
        
        message_length = int.from_bytes(raw_length, 'big')
        
        recv_data = b""
        while len(recv_data) < message_length:
            packet = cs.recv(4096)  
            if not packet:
                raise ValueError("Incomplete data received.")
            recv_data += packet

        # Deserialize the received data
        data_list = pickle.loads(recv_data)
        print("Received data:")
        for entry in data_list:
            print(entry)
        return data_list
    except Exception as e:
        print(f"Error receiving message: {e}")
        return []

def category_list():
    ''' Displays the category list and returns the selected category. '''
    print("Available categories:")
    print("1. Business 2. General 3. Health 4. Science 5. Sports 6. Technology")
    return input("Please enter the category (not the number): ")

def country_list():
    ''' Displays the country list and returns the selected country. '''
    print("Available countries:")
    print("1. au 2. ca 3. jp 4. ae 5. sa 6. kr 7. us 8. ma")
    return input("Please enter the country (not the number): ")

def language_list():
    ''' Displays the language list and returns the selected language. '''
    print("Available languages:")
    print("1. ar 2. en")
    return input("Please enter the language (not the number): ")

def handle_headline_search(cs):
    ''' Handles all headline search-related logic. '''
    while True:
        print("-----------------------------")
        print("- Search headlines menu:")
        print("1. Search for keywords")
        print("2. Search by category")
        print("3. Search by country")
        print("4. List all news headlines")
        print("5. Back to the main menu")

        try:
            option = int(input("Please enter the number of the service: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            message = input("Please enter the keyword: ")
            send_message(cs, f"1-1-{message}")  # Sending keyword search request
            receive_message(cs)

        elif option == 2:
            category = category_list()
            send_message(cs, f"1-2-{category}")  # Sending category search request
            receive_message(cs)

        elif option == 3:
            country = country_list()
            send_message(cs, f"1-3-{country}")  # Sending country search request
            receive_message(cs)

        elif option == 4:
            print("Requesting all headlines.")
            send_message(cs, "1-4")  # Requesting all headlines
            receive_message(cs)

        elif option == 5:
            print("Back to the main menu.")
            break

        else:
            print("Option not on the list.")

def handle_sources_list(cs):
    ''' Handles all list of sources-related logic. '''
    while True:
        print("-----------------------------")
        print("- List of Sources menu:")
        print("1. Search by category")
        print("2. Search by country")
        print("3. Search by language")
        print("4. List all sources")
        print("5. Back to the main menu")

        try:
            option = int(input("Please enter the number of the service: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            category = category_list()
            send_message(cs, f"2-1-{category}")  # Sending category search request
            receive_message(cs)

        elif option == 2:
            country = country_list()
            send_message(cs, f"2-2-{country}")  # Sending country search request
            receive_message(cs)

        elif option == 3:
            language = language_list()
            send_message(cs, f"2-3-{language}")  # Sending language search request
            receive_message(cs)

        elif option == 4:
            print("Requesting all sources.")
            send_message(cs, "2-4")  # Requesting all sources
            receive_message(cs)

        elif option == 5:
            print("Back to the main menu.")
            break

        else:
            print("Option not on the list.")

def main():
    ''' Main client logic for connecting, sending, and receiving messages. '''
    while True:
        # Create a TCP socket
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        try:
            cs.connect(('localhost', 65432))
        except Exception as e:
            print(f"Could not connect to server: {e}")
            break

        # Ask the user for the username, then send it to the server
        username = input("Please enter your username: ")
        send_message(cs, username)

        while True:
            # Print the options for the main menu
            print("-----------------------------")
            print("- Main menu:")
            print("1 - Search headlines")
            print("2 - List of Sources")
            print("3 - Quit")

            try:
                option = int(input("Please enter the number of the service: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if option == 1:
                handle_headline_search(cs)

            elif option == 2:
                handle_sources_list(cs)

            elif option == 3:
                send_message(cs, "Quit")
                cs.close()
                break

            else:
                print("Option not on the list.")

        cs.close()

if __name__ == "__main__":  
    main()
