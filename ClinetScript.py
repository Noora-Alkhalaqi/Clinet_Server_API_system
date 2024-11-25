import socket

# This flag used to stop the main while loop
while True:

    # Creat a socket
    cs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

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
            print("1.1- Search for keywords will allow you to search in the news for a keyword in the news.")
            print("1.2- Search by category will allow you to select the news by category.")
            print("1.3- Search by country will allow you to select news by country")
            print("1.4- List all new headlines will allow you to  select news with no specific preference.")
            print("1.5- Back to the main menu will take you back to the main menu.")

            # Ask the user to enter the option from the Search headlines menu
            option = int(input("please Enter the number of the service: "))
            if option == 1.1:
                input("Please enter the keyword: ")
            elif option == 1.2:
                print("1.Business 2.General 3.Health 4.Science 5.Sports 6.Technology")
                input("From the list above please enter the categoty: ")

            elif option == 1.3:
                print("1.au 2.ca 3.jp 4.ae 5.sa 6.kr 7.us 8.ma")
                input("From the list above please enter the country: ")

            elif option == 1.4:
                print("four")

            elif option == 1.5:
                print("Back to the main menu.")
                break
            # This else is used to handle the error when we have a misentering of a number
            else:
                print("Option not on the list.")

    # The user will be taken to the List of Sources menu when number two is entered
    elif option == 2:
        print("-----------------------------")
        print("-List of Sources menu:")
        print("2.1- Search by category will allow you to select the sources by category.")
        print("2.2- Search by country will allow you to select sources by country")
        print("2.3- Search by language will allow you to select sources language.")
        print("2.4- List all will allow you to select sources with no specific preference")
        print("2.5- Back to the main menu will take you back to the main menu.")

        option = int(input("please Enter the number of the service: "))
        if option == 2.1:
            print("1.Business 2.General 3.Health 4.Science 5.Sports 6.Technology")
            input("From the list above please enter the categoty: ")

        elif option == 2.2:
            print("1.au 2.ca 3.jp 4.ae 5.sa 6.kr 7.us 8.ma")
            input("From the list above please enter the country: ")

        elif option == 2.3:
            print("1.ar 2.en")
            input("From the list above please enter the language: ")

        elif option == 2.4:
            print("four")

        elif option == 2.5:
            print("five")
            break

        # This else is used to handle the error when we have a misentering of a number
        else:
            print("Option not on the list.")

    # This elif is used to quit the program 
    elif option == 3:
        break

    # This else is used to handle the error when we have a misentering of a number
    else:
        print("Option not on the list.")