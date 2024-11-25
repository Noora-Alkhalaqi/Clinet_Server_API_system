import socket

# This flag used to stop the main while loop
while True:

    cs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    # Print the options for the main menu
    print("-----------------------------\n-Main menu:\n1-Search headlines \n2-List of Sources\n3-Quit")
    # Ask the user to enter the number of the option selected
    option = int(input("please Enter the number of the service: "))
    # The user will be taken to the Search headlines menu when number one is entered
    if option == 1:
        while True:
            print("-----------------------------\n-Search headlines menu\n1.1- Search for keywords\n1.2- Search by category\n1.3- Search by country\n1.4- List all new headlines\n1.5- Back to the main menu")
            # Ask the user to enter the option from the Search headlines menu
            option = int(input("please Enter the number of the service: "))
            if option == 1.1:
                print("one")
            elif option == 1.2:
                print("two")
            elif option == 1.3:
                print("three")
            elif option == 1.4:
                print("four")
            elif option == 1.5:
                print("five")
                break
            # This else is used to handle the error when we have a misentering of a number
            else:
                print("Option not on the list.")

    # The user will be taken to the List of Sources menu when number two is entered
    elif option == 2:
        print("-----------------------------\n-List of Sources menu\n2.1- Search by category\n2.2- Search by country\n2.3- Search by language\n2.4- List all\n2.5- Back to the main menu")

        option = int(input("please Enter the number of the service: "))
        if option == 2.1:
            print("one")
        elif option == 2.2:
            print("two")
        elif option == 2.3:
            print("three")
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