# Client and server Script using GUI (ITNE352 Project)

# Project Description
This project involves creating two Python scripts: a client script and a server script.
The client script features a graphical user interface (GUI) that displays a main menu with several submenus for the user to interact with.
The server script listens for incoming requests from the client and responds by retrieving relevant news data from an external API using NewsAPI (https://newsapi.org/)

**Group**: A16

**Course code**: ITNE352

**Section**: 1

**Semester**: First Semester 2024-2025

**Student names & IDs:**
1. Name: Hawra Fadhel Abbas           ID: 202208944 
2. Name: Noora Salah Alkhalaqi        ID: 202209541

## Table of Contents:
1. Requirements
2. How to run the system
3. Explanation of clientScript.py 
4. Explanation of serverScript.py 
5. Additional concepts
6. Acknowledgments
7. Conclusion


## Requirements
1. Python 3 must be installed on your system (https://www.python.org/downloads/)
2. Download all files needed from the repository (https://github.com/HawraFadhel/ITNE352-Project)
3. Install the required libraries by running the following command in your terminal: pip install tkinter requests json
4. Use a text editor or IDE to open the clientScript.py and serverScript.py files and run them using
5. Additional packeges used: requests packeges, use pip install requests command to install it in your system and PIL packeges, use pip install pillow command to install it in your system

## How to run the system
Open the files in your text editor we used ViVisual Studio Code for this project. Secondly , run the serverScript.py file first, then run the clientScript.py file. The client will Gui interface will be display and you can interact with it. The server will listen for incoming requests from the client and respond by retrieving relevant news data from an external API using NewsAPI.

## Explanation of clientScript.py
The client script is a GUI application that allows users to interact with the server.
To run the Client side we import the following libraries: 
from tkinter import *
from PIL import Image, ImageTk
import socket
import pickle
import tkinter as tk
from tkinter import messagebox, Listbox
and each one of these have it own usage.

Functions that is implmented in the client script:

- def __init__(self) : This function is used to initialize the client application.

- def initialize_gui(self): This function is used to initialize the GUI application.

- def clear_window(self): This function is used to clear the window.

- def connect_to_server(self): This function is used to connect to the server.

- def send_message(self, message): This function is used to send a message to the server.

- def show_main_menu(self): This function is used to show the main menu of the application.

- def show_headlines_menu(self): This function is used to show the headlines menu of the application.

- def show_sources_menu(self): This function is used to show the sources menu of the application.

- def show_category_buttons(self): This function is used to show the category buttons of the application.

- def show_country_buttons(self): This function is used to show the country buttons of the application.

- def show_language_buttons(self): Displays buttons for language search.

- def show_keyword_input(self): Displays input field for keyword search.

- def submit_keyword(): This function is used to submit the keyword search and it is inside the show_keyword_input function.

All functions above are used to create the GUI application and to interact with the server and are included in a NewsClientGUI.

This is our main: 
if __name__ == "__main__":
    app = NewsClientGUI()
    app.root.mainloop()
will save the application in a variable call app and run it using the mainloop method.

The GUI works as follows:
It will display the welcome message and will ask the user for the user name, then it will display the main menu of the application. The main menu will have the following options: Headlines, Sources, Categories, Countries, Languages, and Keyword Search. Each option will have its own GUI window. The user can interact with the server by selecting the options and entering the required information to get the news. The user can also exit the application by selecting the exit option or get more details about the news by clicking on view details.

## Explanation of serverScript.py 
The serverScript.py handles communication between the client and the News API. It listens for client requests, retrieves news data (like headlines or sources) from the API, and sends the response back to the client.

- Key functions:

Socket Communication: The server uses Python's socket library to create a TCP server that listens for incoming connections on a specified port (65432). When a client connects, the server accepts the connection and starts a new thread to handle the interaction with the client.

Multithreading: The server can handle multiple clients simultaneously using threads. Each client’s requests are handled in separate threads, ensuring that the server remains responsive even with multiple users.

Request Parsing: When the server receives a request, it parses the request string (which includes parameters such as the request type and search criteria). Based on the request, it constructs the appropriate API query for fetching news data.

Data Fetching: The server sends a request to the News API (https://newsapi.org/) with the appropriate parameters (such as category, country, or keyword) and retrieves the news data in JSON format. If the request is successful, the server processes the data and extracts relevant details such as the article title, source, description, and publication date.

Data Response: After processing the data, the server sends the news articles (or sources) back to the client in a serialized format using pickle. The client can then display the results in the user interface.

Error Handling: The server handles any errors that occur during the request process, such as network errors or invalid API responses, and returns appropriate error messages to the client.

Data Saving: For each client request, the server saves the fetched data into a JSON file, which includes details like the client’s name, request type, and the results fetched. This provides a record of the requests and the data returned.

## Additional concepts
We used GUI as an Additional concept for this project and learned how to use it in Python, probably in our project.
This is the code for our main window aka (the first window the user will see and interact with):

def initialize_gui(self):
        """Initialize GUI with Login Screen."""
        self.clear_window()

        tk.Label(self.root, text="Welcome to the News System ", fg="#276183", bg = "#B8E2F2", font=("Arial", 16, "italic", "bold")).pack(pady=20)
        
        image = Image.open("Newsimg.png")
        image = image.resize((100, 100))  
        self.photo = ImageTk.PhotoImage(image) 

        l1 = tk.Label(self.root, image=self.photo, bg = "#B8E2F2").pack(pady=5)

        tk.Label(self.root, text="Enter your username:", fg="#276183" , bg = "#B8E2F2", font = 14).pack(pady=10)

        self.username_entry = tk.Entry(self.root , bd=0)
        self.username_entry.pack(pady=10)

        tk.Button(self.root, text="Connect to Server", command=self.connect_to_server).pack(pady=20)

The user will see the welcome message alongside a photo and will be asked to enter his username. After entering the username, the user can navigate between different screens (windows) until selecting the "Quit" option, which will terminate the connection and close the client. 

## Acknowledgments
I would like to express my sincere gratitude to Dr.Mohamed A. Almeer for his help throughout this project. And I also appreciate the teamwork that made this project possible.

## Conclusion
Through the development of this project, we have gained hands-on experience with implementing a server -client architecture using Python's socket library and GUI programming using Tkinter and many other things. We also faced a lot of difficulties and challenges but we were able to overcome them and complete the project successfully. I hope that this project will serve as a valuable learning experience for anyone who reads it.