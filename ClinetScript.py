import socket
import pickle

def send_message(cs, message):
    ''' Sends the message to the server. '''
    try:
        cs.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(cs):
    ''' Receives the message from the server. '''
    try:
        recv_data = cs.recv(4096)  # Increased buffer size to handle larger messages
        if not recv_data:
            print("No data received. Connection may have been closed.")
            return
        
        # Deserialize the received data
        data_list = pickle.loads(recv_data)
        for entry in data_list:
            print(entry)
    except Exception as e:
        print(f"Error receiving message: {e}")

def category_list():
    ''' Displays the category list and returns the selected category. '''
    print("1. Business 2. General 3. Health 4. Science 5. Sports 6. Technology")
    message = input("From the list above please enter the category (not the number): ")
    return message

def country_list():
    ''' Displays the country list and returns the selected country. '''
    print("1. au 2. ca 3. jp 4. ae 5. sa 6. kr 7. us 8. ma")
    message = input("From the list above please enter the country (not the number): ")
    return message

def language_list():
    ''' Displays the language list and returns the selected language. '''
    print("1. ar 2. en")
    message = input("From the list above please enter the language (not the number): ")
    return message

while True:
    # Create a TCP socket
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    cs.connect(('localhost', 65432))

    # Ask the user for the username, then send it to the server
    username = input("Please enter your username: ")
    send_message(cs, username)

    # Print the options for the main menu
    print("-----------------------------")
    print("- Main menu:")
    print("1 - Search headlines")
    print("2 - List of Sources")
    print("3 - Quit")

    # Ask the user to enter the number of the option selected
    try:
        option = int(input("Please enter the number of the service: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    # Handle search headlines menu
    if option == 1:
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
                send_message(cs, "1-4-")  # Requesting all headlines
                receive_message(cs)

            elif option == 5:
                print("Back to the main menu.")
                break

            else:
                print("Option not on the list.")

    # Handle list of sources menu
    elif option == 2:
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
                send_message(cs, "2-4-")  # Requesting all sources
                receive_message(cs)

            elif option == 5:
                print("Back to the main menu.")
                break

            else:
                print("Option not on the list.")

    # Handle quit option
    elif option == 3:
        send_message(cs, "Quit")
        cs.close()
        break

    else:
        print("Option not on the list.")