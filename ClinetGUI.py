import socket
import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox

class NewsClientGUI:
    def __init__(self):
        self.cs = None
        self.username = None

        # Create the root window
        self.root = tk.Tk()
        self.root.title("News Client")
        self.root.geometry("600x400")

        # Initialize the GUI
        self.initialize_gui()

    def initialize_gui(self):
        """Initialize GUI with Login Screen."""
        self.clear_window()

        tk.Label(self.root, text="Welcome to the News Client", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter your username:").pack(pady=10)

        self.username_entry = tk.Entry(self.root)
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

        tk.Label(self.root, text="Main Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Search Headlines", command=self.show_headlines_menu).pack(pady=10)
        tk.Button(self.root, text="List of Sources", command=self.show_sources_menu).pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.quit_client).pack(pady=20)

    def show_headlines_menu(self):
        """Displays the headlines menu."""
        self.clear_window()

        tk.Label(self.root, text="Headlines Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Search for Keywords", command=lambda: self.headlines_action("1-1")).pack(pady=10)
        tk.Button(self.root, text="Search by Category", command=lambda: self.headlines_action("1-2")).pack(pady=10)
        tk.Button(self.root, text="Search by Country", command=lambda: self.headlines_action("1-3")).pack(pady=10)
        tk.Button(self.root, text="List All Headlines", command=lambda: self.headlines_action("1-4")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def show_sources_menu(self):
        """Displays the sources menu."""
        self.clear_window()

        tk.Label(self.root, text="Sources Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Search by Category", command=lambda: self.sources_action("2-1")).pack(pady=10)
        tk.Button(self.root, text="Search by Country", command=lambda: self.sources_action("2-2")).pack(pady=10)
        tk.Button(self.root, text="Search by Language", command=lambda: self.sources_action("2-3")).pack(pady=10)
        tk.Button(self.root, text="List All Sources", command=lambda: self.sources_action("2-4")).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def headlines_action(self, action_code):
        """Handles actions related to headlines."""
        input_value = None
        if action_code == "1-1":  # Keyword search
            input_value = self.get_user_input("Enter Keyword")
            if not input_value:
                return
        elif action_code == "1-2":  # Category search
            input_value = self.get_user_input("Enter Category")
        elif action_code == "1-3":  # Country search
            input_value = self.get_user_input("Enter Country")
        elif action_code == "1-4":  # All headlines
            input_value = None

        if input_value:
            self.send_message(f"{action_code}-{input_value}")
        else:
            self.send_message(action_code)

        data_list = self.receive_message()
        self.display_results(data_list, "Headlines")

    def sources_action(self, action_code):
        """Handles actions related to sources."""
        input_value = None
        if action_code in ["2-1", "2-2", "2-3"]:  # Requires category, country, or language
            input_value = self.get_user_input("Enter your choice")
            if not input_value:
                return

        if input_value:
            self.send_message(f"{action_code}-{input_value}")
        else:
            self.send_message(action_code)

        data_list = self.receive_message()
        self.display_results(data_list, "Sources")

    def get_user_input(self, prompt):
        """Get user input via a popup."""
        return simpledialog.askstring("Input", prompt)

    def display_results(self, data_list, result_type):
        """Displays results in a new window."""
        result_window = tk.Toplevel(self.root)
        result_window.title(f"{result_type} Results")
        result_window.geometry("800x600")

        tk.Label(result_window, text=f"{result_type} Results", font=("Arial", 16)).pack(pady=10)

        if not data_list:
            tk.Label(result_window, text="No results found.").pack(pady=10)
        else:
            result_list = Listbox(result_window, width=100, height=25)
            for idx, entry in enumerate(data_list, start=1):
                result_list.insert(idx, f"{idx}. {entry.get('title', entry.get('name', 'Unknown'))}")
            result_list.pack(pady=10)

            def view_details():
                selected = result_list.curselection()
                if not selected:
                    messagebox.showwarning("Warning", "No item selected.")
                    return
                details = data_list[selected[0]]
                self.display_details(details)

            tk.Button(result_window, text="View Details", command=view_details).pack(pady=10)

    def display_details(self, details):
        """Display details of a selected item."""
        details_window = tk.Toplevel(self.root)
        details_window.title("Details")

        for key, value in details.items():
            tk.Label(details_window, text=f"{key}: {value}").pack(anchor='w', padx=10, pady=5)

    def quit_client(self):
        """Handles client quitting."""
        if self.cs:
            self.send_message("Quit")
            self.cs.close()
        self.root.quit()

if __name__ == "__main__":
    app = NewsClientGUI()
    app.root.mainloop()