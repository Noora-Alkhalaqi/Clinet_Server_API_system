import socket

def send_message(cs, message):
    '''
      This function will send the message to the server.    
    '''
    # Use try and except to handel any error in the sending process
    try:
        cs.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(cs):
    ''' 
    This function will receive the message from the server. 
    '''
    while True:
        recv_data = cs.recv(1024)
        print(cs.decode('ascii'))
        if not cs:
            break

while True:

    # Creat a Tcp socket
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # this address will be change
    cs.connect(('localhost', 65432))

    # Ask the user for the user name then send it to the server
    username = input("Please enter your username: ")
    send_message(cs, username)

    # Print the options for the main menu
    print("-----------------------------")
    print("-Main menu:")
    print("1-Search headlines will takes you to the Headlines menu.")
    print("2-List of Sources will take you to the Sources menue.")
    print("3-Quit will terminates the connection and client")

    # Ask the user to enter the number of the option selected
    option = int(input("please Enter the number of the service: "))

    # The user will be taken to the Search headlines menu when number one is entered
    if option == 1:
        while True:
            print("-----------------------------")
            print("-Search headlines menu:")
            print("1. Search for keywords will allow you to search in the news for a keyword in the news.")
            print("2. Search by category will allow you to select the news by category.")
            print("3. Search by country will allow you to select news by country")
            print("4. List all new headlines will allow you to  select news with no specific preference.")
            print("5. Back to the main menu will take you back to the main menu.")

            # Ask the user to enter the option from the Search headlines menu
            option = int(input("please Enter the number of the service: "))
            if option == 1:
                message = input("Please enter the keyword: ")
                send_message(cs, message)
                receive_message(cs)

            elif option == 2:
                print("1.Business 2.General 3.Health 4.Science 5.Sports 6.Technology")
                message = input("From the list above please enter the categoty: ")
                send_message(cs, message)
                receive_message(cs)

            elif option == 3:
                print("1.au 2.ca 3.jp 4.ae 5.sa 6.kr 7.us 8.ma")
                message = input("From the list above please enter the country: ")
                send_message(cs, message)
                receive_message(cs)

            elif option == 4:
                print("four")

            elif option == 5:
                print("Back to the main menu.")
                break
            # This else is used to handle the error when we have a misentering of a number
            else:
                print("Option not on the list.")

    # The user will be taken to the List of Sources menu when number two is entered
    elif option == 2:
        print("-----------------------------")
        print("-List of Sources menu:")
        print("1. Search by category will allow you to select the sources by category.")
        print("2. Search by country will allow you to select sources by country")
        print("3. Search by language will allow you to select sources language.")
        print("4. List all will allow you to select sources with no specific preference")
        print("5. Back to the main menu will take you back to the main menu.")

        option = int(input("please Enter the number of the service: "))
        if option == 1:
            print("1.Business 2.General 3.Health 4.Science 5.Sports 6.Technology")
            message = input("From the list above please enter the categoty: ")
            send_message(cs, message)
            receive_message(cs)

        elif option == 2:
            print("1.au 2.ca 3.jp 4.ae 5.sa 6.kr 7.us 8.ma")
            message = input("From the list above please enter the country: ")
            send_message(cs, message)
            receive_message(cs)

        elif option == 3:
            print("1.ar 2.en")
            message = input("From the list above please enter the language: ")
            send_message(cs, message)
            receive_message(cs)

        elif option == 4:
            print("four")

        elif option == 5:
            print("five")
            break

        # This else is used to handle the error when we have a misentering of a number
        else:
            print("Option not on the list.")

    # This elif is used to quit the program 
    elif option == 3:
        # Close the Socket
        cs.close()
        break

    # This else is used to handle the error when we have a misentering of a number
    else:
        print("Option not on the list.")