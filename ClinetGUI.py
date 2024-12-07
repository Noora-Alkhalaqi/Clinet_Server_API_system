import socket
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pickle
import sys

class NewsForClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.text_value = ""
        self.scroll_enabled = False

        # Setup GUI root
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.configure(background="#DFC5FE")
        self.root.title("News For Clinet")
        self.labels = []
        self.frame = None
        self.entry = None
        self.button = None

    def connect_to_server(self):
        """Attempt to connect to the server."""
        try:
            self.client_socket.connect((self.server_host, self.server_port))
        except Exception as e:
            self.display("Server not available, try again later.", pad=(200, 5))
            messagebox.showerror("Connection Error", str(e))
            sys.exit(1)

    def send_data(self, data):
        """Send data to the server."""
        self.client_socket.send(data.encode('ascii'))

    def receive_data(self):
        """Receive data from the server."""
        try:
            data = self.client_socket.recv(10000)
            return pickle.loads(data)
        except Exception as e:
            messagebox.showerror("Receive Error", str(e))
            return []

    def display(self, text, pad=(5, 5), font_size=25):
        """Display text in the GUI."""
        label = tk.Label(
            self.root,
            text=text,
            bg="#8e6abd",
            font=("Comic Sans MS", font_size),
        )
        label.pack(pady=pad)
        self.labels.append(label)

    def get_text(self):
        """Retrieve text entered by the user."""
        self.text_value = self.entry.get()
        self.clear_interface()

    def clear_interface(self):
        """Clear the interface."""
        for label in self.labels:
            label.destroy()
        self.labels.clear()
        if self.entry:
            self.entry.destroy()
        if self.button:
            self.button.destroy()
        if self.frame:
            self.frame.destroy()

    def input_text(self, placeholder="Enter text here..."):
        """Input text with an entry and button."""
        self.entry = ctk.CTkEntry(
            self.root,
            placeholder_text=placeholder,
            width=400,
            height=60,
            border_width=0,
            corner_radius=20,
            fg_color="white",
            text_color="black",
            font=("Comic Sans MS", 25),
        )
        self.entry.pack(pady=(10, 5))

        self.button = ctk.CTkButton(
            self.root,
            text="Send",
            command=self.get_text,
            fg_color="white",
            text_color="black",
            font=("Comic Sans MS", 25),
        )
        self.button.pack(pady=(5, 10))

        self.root.mainloop()

    def run(self):
        """Run the main application."""
        try:
            self.display("Welcome to our syatem!", pad=(200, 20), font_size=35)
            self.display("Please Enter your username:")
            self.input_text()
            client_name = self.text_value
            self.connect_to_server()
            self.send_data(client_name)

            # Main loop for menu interaction
            while True:
                self.display("Main Menu", font_size=35, pad=(100, 10))
                self.display("1. Search a headline\n2. List sources\n3. Quit", pad=(5, 10))
                self.display("Enter your choice:")
                self.input_text()
                choice = self.text_value.strip()

                if choice == "3":
                    self.send_data("Quit")
                    self.display("Goodbye!", pad=(200, 5))
                    break

                elif choice == "1":
                    while True:
                        scroll = False
                        # to display the search_headlines_menu and  enable user to enter a choice
                        self.display("Menu", 40, pad)
                        self.display("1. Search for Keywords\n2. Search by Category\n3. Search by Country\n4. List All New Headlines\n5. Back to Main Menu",pad=(5, 10),)
                        self.display("Enter your choice number: ")
                        self.input_text()
                        pad = (180,5)
                        choice = self.text_value.strip()
                        # Make sure the choice is valid (from 1-4: 1. Search for keywords | 2. Search by category | 3. Search by country | 4. List all new headlines)
                        if choice < "1" and choice > "4":
                            key = ''
                            if choice == '1': # 1. Search for keywords
                                self.display('Enter a keyword: ',(200,5))
                                self.display('# -1 to go back in menu')
                                self.input_text()
                                key = self.text_value.strip()

                                if key == "-1": # if key = -1 to go back in menu
                                    break
                            elif choice == '2': # 2. Search by category 
                                while True:
                                    categories = ["Business", "General", "Health", "Science", "Sports", "Technology"]
                                    self.display('Enter a category: ',pad) 
                                    self.display("# available categories: \n 1. Business 2. General 3. Health 4. Science 5. Sports 6. Technology")
                                    self.display('# -1 to go back in menu')
                                    self.input_text()
                                    key = self.text_value.strip()
                                    if key in categories or key == "-1":
                                        break
                                    else:
                                        self.display("No such category, try again.",(200,5))     
                                        pad = 5

                            elif choice == '3': # 3. Search by country
                                while True:
                                    countries = ["Australia", "Canada", "Japan", "United arab emirates", "Saudi arabia", "South korea","United states","Morocco"]
                                    self.display('Enter a country: ',pad) 
                                    self.display("Available countries: \n 1.Australia \n 2. Canada \n 3. Japan \n 4. United arab emirates\n 5. Saudi arabia \n 6. South korea \n 7. United states \n 8. Morocco " , 16, 5)
                                    self.display('# -1 to go back in menu')
                                    self.input_text()
                                    key = self.text_value.strip()
                                    if key in countries or key == "-1":
                                        if key == "Australia":
                                            key = "au"
                                        elif key == "Canada":
                                            key = "ca"
                                        elif key == "Japan": 
                                            key = "jp"
                                        elif key == "United arab emirates":
                                            key = "ae"
                                        elif key == "Saudi arabia":
                                            key = "sa"
                                        elif key == "South korea": 
                                            key = "kr"
                                        elif key == "United states":
                                            key = "us"
                                        elif key == "Morocco":
                                            key = "ma"
                                        break
                                    else:
                                        self.display("No such country, try again.",(200,5))  
                                        pad = 5  

                            elif choice == '4':
                                self.display("List All New Headlines.",pad)
                                key = "4"

                        if key == "-1":
                            break
                        
                        # sending and recieving
                        choice += "-1"
                        choice += "-"+key # Here the key can be a keyword / category / country...
                        received_list = []
                        self.send_data(choice) # Choice format is : (headline_menu choice) -1 -(key)
                        received_data = self.receive_data()
                        #pickle is used so the received_list receives as a list not str
                        received_list = pickle.loads(received_data)

                        for data in received_list:
                            self.display(data,pad)
                            self.display("\n")
                        
                        
                        if received_list[0] == ["no news found, or server is not reachable."]:
                            response = "no news found, or server is not reachable."
                            self.display(response)
                            pad = 5
                        
                        elif choice == '5':
                            break
                        else:
                            self.display("No such choice, try again.",(100,5))
                            pad = 5


                elif choice == "2":
                    self.display("List sources:")

                else:
                    self.display("Invalid choice, try again.", pad=(100, 5))

        except Exception as e:
            messagebox.showerror("Application Error", str(e))
        finally:
            self.client_socket.close()
            self.root.destroy()


if __name__ == "__main__":
    client = NewsForClient(server_host="localhost", server_port=65432)
    client.run()