from tkinter import *
from PIL import Image, ImageTk
import socket
import pickle
import tkinter as tk
from tkinter import messagebox, Listbox

class NewsClientGUI:
    def __init__(self):
        self.cs = None
        self.username = None

        # Create the root window
        self.root = tk.Tk()
        self.root.title("News Client")
        self.root.geometry("600x400")
        self.root.configure(background="#B8E2F2")

        # Initialize the GUI
        self.initialize_gui()

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

    def clear_window(self):
        """Clears all widgets in the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def connect_to_server(self):
        """Handles server connection logic."""
        self.username = self.username_entry.get()
        if not self.username.strip():
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        try:
            # Initialize socket connection
            self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cs.connect(('localhost', 65432))
            self.send_message(self.username)
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")

    def send_message(self, message):
        """Send message to the server."""
        try:
            self.cs.sendall(message.encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def receive_message(self):
        """Receive message from the server."""
        try:
            raw_length = self.cs.recv(4)
            if not raw_length:
                raise ValueError("No data received. Connection may have been closed.")
            message_length = int.from_bytes(raw_length, 'big')
            recv_data = b""
            while len(recv_data) < message_length:
                packet = self.cs.recv(4096)
                if not packet:
                    raise ValueError("Incomplete data received.")
                recv_data += packet
            return pickle.loads(recv_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to receive data: {e}")
            return []

    def show_main_menu(self):
        """Displays the main menu."""
        self.clear_window()

        tk.Label(self.root, text="Main Menu", font=("Arial", 16,"italic","bold"), fg="#276183", bg = "#B8E2F2").pack(pady=20)
        tk.Button(self.root, text="Search Headlines", command=self.show_headlines_menu).pack(pady=10)
        tk.Button(self.root, text="List of Sources", command=self.show_sources_menu).pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.quit_client).pack(pady=20)

    def show_headlines_menu(self):
        """Displays the headlines menu."""
        self.clear_window()

        tk.Label(self.root, text="Headlines Menu", font=("Arial", 16,"italic","bold"), fg="#276183", bg = "#B8E2F2").pack(pady=20)
        tk.Button(self.root, text="Search for Keywords", command=self.show_keyword_input).pack(pady=10)
        tk.Button(self.root, text="Search by Category", command=self.show_category_buttons).pack(pady=10)
        tk.Button(self.root, text="Search by Country", command=self.show_country_buttons).pack(pady=10)
        tk.Button(self.root, text="List All Headlines", command=lambda: self.headlines_action("1-4")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def show_sources_menu(self):
        """Displays the sources menu."""
        self.clear_window()

        tk.Label(self.root, text="Sources Menu", font=("Arial", 16,"italic","bold"), fg="#276183", bg = "#B8E2F2").pack(pady=20)
        tk.Button(self.root, text="Search by Category", command=self.show_category_buttons).pack(pady=10)
        tk.Button(self.root, text="Search by Country", command=self.show_country_buttons).pack(pady=10)
        tk.Button(self.root, text="Search by Language", command=self.show_language_buttons).pack(pady=10)
        tk.Button(self.root, text="List All Sources", command=lambda: self.sources_action("2-4")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def show_category_buttons(self):
        """Displays buttons for category search."""
        self.clear_window()

        categories = ["business", "general", "health", "science", "sports", "technology"]
        for category in categories:
            tk.Button(self.root, text=category.capitalize(), command=lambda c=category: self.categories_action(c)).pack(pady=5)
        tk.Button(self.root, text="Back to Headlines Menu", command=self.show_headlines_menu).pack(pady=20)

    def show_country_buttons(self):
        """Displays buttons for country search."""
        self.clear_window()

        countries = ["au", "ca", "jp", "ae", "sa", "kr", "us", "ma"]
        for country in countries:
            tk.Button(self.root, text=country.upper(), command=lambda c=country: self.headlines_action(f"1-3-{c}")).pack(pady=5)
        tk.Button(self.root, text="Back to Headlines Menu", command=self.show_headlines_menu).pack(pady=20)

    def show_language_buttons(self):
        """Displays buttons for language search."""
        self.clear_window()

        languages = ["ar", "en"]
        for language in languages:
            tk.Button(self.root, text=language.upper(), command=lambda l=language: self.sources_action(f"2-3-{l}")).pack(pady=5)
        tk.Button(self.root, text="Back to Sources Menu", command=self.show_sources_menu).pack(pady=20)

    def show_keyword_input(self):
        """Displays a text field for keyword input."""
        self.clear_window()

        tk.Label(self.root, text="Enter Keyword to Search", font=("Arial", 16), fg="#276183", bg = "#B8E2F2").pack(pady=20)

        keyword_entry = tk.Entry(self.root, width=50 , bd=0)
        keyword_entry.pack(pady=10)

        def submit_keyword():
            keyword = keyword_entry.get()
            if keyword.strip():
                self.headlines_action(f"1-1-{keyword}")
            else:
                messagebox.showwarning("Input Error", "Please enter a valid keyword.")
        
        tk.Button(self.root, text="Search", command=submit_keyword).pack(pady=10)
        tk.Button(self.root, text="Back to Headlines Menu", command=self.show_headlines_menu).pack(pady=20)

    def headlines_action(self, action_code):
        """Handles actions related to headlines."""
        self.send_message(action_code)
        data_list = self.receive_message()
        self.display_results(data_list, "Headlines")

    def categories_action(self, category):
        """Handles category search."""
        self.send_message(f"1-2-{category}")
        data_list = self.receive_message()
        self.display_results(data_list, "Headlines")

    def sources_action(self, action_code):
        """Handles actions related to sources."""
        self.send_message(action_code)
        data_list = self.receive_message()
        self.display_results(data_list, "Sources")

    def display_results(self, data_list, result_type):
        """Displays results in a new window."""
        result_window = tk.Toplevel(self.root)
        result_window.title(f"{result_type} Results")
        result_window.geometry("800x600")

        tk.Label(result_window, text=f"{result_type} Results", font=("Arial", 16), fg="#276183", bg = "#B8E2F2").pack(pady=10)

        if not data_list:
            tk.Label(result_window, text="No data found.", font=("Arial", 12), fg="red", bg = "#B8E2F2").pack(pady=10)
        else:
            result_list = Listbox(result_window, width=100, height=25)
            for idx, entry in enumerate(data_list, start=1):
                # Check if entry is a dictionary and contains a title or name
                if isinstance(entry, dict):
                    result_list.insert(idx, f"{idx}. {entry.get('title', entry.get('name', 'Unknown'))}")
                else:
                    result_list.insert(idx, f"{idx}. {entry}")  # In case it's a simple string or list entry
            result_list.pack(pady=10)

        def view_details():
            selected = result_list.curselection()
            if not selected:
                messagebox.showwarning("Warning", "No item selected.")
                return
            details = data_list[selected[0]]
            self.display_details(details)

        def go_back():
            result_window.destroy()

        # Create "View Details" and "Back" buttons side by side
        button_frame = tk.Frame(result_window)
        button_frame.pack(pady=20)

        view_button = tk.Button(button_frame, text="View Details", command=view_details)
        view_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(button_frame, text="Back", command=go_back)
        back_button.pack(side=tk.LEFT, padx=10)

    def display_details(self, details):
        """Display details of a selected item."""
        details_window = tk.Toplevel(self.root)
        details_window.title("Details")

        for key, value in details.items():
            tk.Label(details_window, text=f"{key}: {value}", background="#B8E2F2").pack(anchor='w', padx=10, pady=5)


    def quit_client(self):
        """Handles client quitting."""
        if self.cs:
            self.send_message("Quit")
            self.cs.close()
        self.root.quit()

if __name__ == "__main__":
    app = NewsClientGUI()
    app.root.mainloop()