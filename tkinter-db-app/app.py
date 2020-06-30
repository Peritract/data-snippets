# Import statements
import tkinter as tk  # For the UI
import tkinter.ttk as ttk  # For the UI (fancier buttons)
import tkinter.messagebox as messagebox  # For displaying status/error messages
import sqlite3 as sql  # Interact with the database
import os, sys  # Manage file paths
base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

class Application(tk.Tk):
    """Base application class, holding all the UI frames"""

    def __init__(self):
        """Initial set-up"""
        # Make connections to root tk object
        super().__init__()

        # Set up the database

        # Create the right paths
        base_dir = '.'
        if hasattr(sys, '_MEIPASS'):
            base_dir = os.path.join(sys._MEIPASS)

        self.database_name = os.path.join(base_dir, "database.db")
        self.setup_database()

        # Create holder element for all the UI frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create dictionary to hold references to each frame
        self.frames = {}

        # Set up main Frame
        self.Frame_setup()

        # Create the UI frames
        self.create_frames()

        # Move the main menu to the top
        self.show_frame("MainMenuFrame")

        # Add the frame container to the interface
        self.container.pack()

    def create_frames(self):
        """Initialise the frames and add them to the holder"""
        for frame in [MainMenuFrame, InputDataFrame, ViewDataFrame]:
            frame_object = frame(parent=self.container, controller=self)
            self.frames[frame.__name__] = frame_object
            frame_object.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame):
        """Move a frame to the top of the stack and display it"""
        self.frames[frame].tkraise()

        # Run the UI update function for that frame
        self.frames[frame].update_UI()

    def quit(self):
        self.destroy()

    def Frame_setup(self):
        """Set general Frame properties"""
        self.title("Data Analysis Tool")
        self.geometry("400x300")
        self.resizable(False, False)

    def show_error(self, message):
        """Generic error popup"""
        messagebox.showerror("ERROR", message)

    def show_alert(self, message):
        """Generic alert popup"""
        messagebox.showinfo("INFO", message)

    def setup_database(self):
        """Creates the database table if it doesn't already exist"""

        # Query to create the table
        query = """
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created DATE NOT NULL
            )
        """

        # Open a connection
        # the "with" keyword closes the connection automatically when done.
        with sql.connect(self.database_name) as conn:
            # Run the query
            conn.execute(query)

    def insert_message_to_database(self, message, author):
        """Inserts a new message into the database"""

        # Create the query
        query = f"""
            INSERT INTO message (content, author, created)
            VALUES ('{message}', '{author}', date('now'));
        """

        # Open a connection
        # the "with" keyword closes the connection automatically when done.
        with sql.connect(self.database_name) as conn:

            try:
                # Run the query
                conn.execute(query)

                return "success"

            except sql.Error as error:

                # Report the problem
                return error

    def extract_message_data(self):
        """Retrieves data from the database"""

        # Create the query
        query = f"""
            SELECT * FROM message;
        """

        # Open a connection
        # the "with" keyword closes the connection automatically when done.
        with sql.connect(self.database_name) as conn:

            try:
                # Create a cursor object
                cursor = conn.cursor()

                # Run the query
                cursor = conn.execute(query)

                # Return all the results
                # Wrapped in a tuple for error handling later
                return ("success", cursor.fetchall())

            except sql.Error as error:

                # Report the problem
                return (error, None)


class MainMenuFrame(tk.Frame):
    """Class for the main menu and its elements"""

    def __init__(self, parent, controller):
        """Create connections to the parent and root objects"""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create UI elements
        self.create_elements()

        # Display the menu
        self.pack(side="top", fill="both", expand=True)

    def create_elements(self):
        """Create and position all elements"""

        title = tk.Label(self, text="Main Menu")
        description = tk.Label(
            self, text="An example of working with TKinter and .csvs")

        input_button = ttk.Button(self, text="Add data to the database",
                                  command=lambda:
                                  self.controller.show_frame("InputDataFrame"))

        view_button = ttk.Button(self, text="View data in the database",
                                 command=lambda:
                                 self.controller.show_frame("ViewDataFrame"))

        quit_button = ttk.Button(self, text="Quit program",
                                 command=self.controller.quit)

        # Position elements

        for i in range(0, 8):
            self.grid_columnconfigure(i, weight=1)

        title.pack(fill=tk.X, pady=5)
        description.pack(fill=tk.X, pady=5)
        input_button.pack(fill=tk.X, padx=40, pady=5)
        view_button.pack(fill=tk.X, padx=40, pady=5)
        quit_button.pack(fill=tk.X, padx=40, pady=5)

    def update_UI(self):
        """Make immediate updates when the frame is loaded in"""

        # Reset the Frame size
        self.controller.geometry('400x300')
        self.focus_force()


class InputDataFrame(tk.Frame):
    """Class for the input data window"""

    def __init__(self, parent, controller):
        """Create connections to the parent and root objects"""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Variables/elements for the input data
        self.author = tk.StringVar()
        self.message = tk.Text(self, height=4, wrap="word",
                               highlightbackground="black",
                               highlightthickness=1)

        # Create UI elements
        self.create_elements()

        # Display the menu
        self.grid()

    def create_elements(self):
        """Create and position all elements"""

        title = tk.Label(self, text="Input data")
        description = tk.Label(self, text="Add data to the database")

        # Message box and label
        message_label = tk.Label(self, text="Message:")

        # Author box and label
        author_holder = tk.Frame(self)
        author = tk.Entry(author_holder, textvariable=self.author)
        author_label = tk.Label(author_holder, text="Author:")

        input_button = ttk.Button(self, text="Input data",
                                  command=lambda: self.input_data())

        back_button = ttk.Button(self, text="Back",
                                 command=lambda:
                                 self.controller.show_frame("MainMenuFrame"))

        # Position elements
        title.pack(fill=tk.X, pady=5)
        description.pack(fill=tk.X, pady=5)

        message_label.pack(fill=tk.X, padx=5)
        self.message.pack(expand="YES", fill="both", padx=5)

        author_label.pack(side=tk.LEFT, padx=5)
        author.pack(side=tk.LEFT, padx=5)
        author_holder.pack(fill=tk.X, padx=40, pady=5)

        input_button.pack(fill=tk.X, padx=40, pady=5)
        back_button.pack(fill=tk.X, padx=40, pady=5)

    def input_data(self):
        """Adds data to the database"""

        # Grab the values from the variables
        message = self.message.get(1.0, "end")
        author = self.author.get()

        # If both values are present
        if len(message) > 0 and len(author) > 0:
            # Send the message to the database
            result = self.controller.insert_message_to_database(message,
                                                                author)

            # Check the result
            if result == "success":
                self.controller.show_alert("Database row inserted.")
                # Clear the variables
                self.message.delete(1.0, "end")
                self.author.set("")
            else:
                details = result.args
                self.controller.show_error(f"Database error! Error: {details}")

        else:
            self.controller.show_error("Both values need to be present.")

    def update_UI(self):
        """Make immediate updates when the frame is loaded in"""

        # Reset the Frame size
        self.controller.geometry('400x300')
        self.focus_force()


class ViewDataFrame(tk.Frame):
    """Class for the viewing data window"""

    def __init__(self, parent, controller):
        """Create connections to the parent and root objects"""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Display table
        self.table = ttk.Treeview(self, columns=("message", "author", "date"))

        # Create UI elements
        self.create_elements()

        # Display the menu
        self.grid()

    def create_elements(self):
        """Create and position all elements"""

        title = tk.Label(self, text="Input data")
        description = tk.Label(self, text="View data in the database")

        update_button = ttk.Button(self, text="Update",
                                   command=self.refresh_data)

        back_button = ttk.Button(self, text="Back",
                                 command=lambda:
                                 self.controller.show_frame("MainMenuFrame"))

        # Position elements
        title.pack(fill=tk.X, pady=5)
        description.pack(fill=tk.X, pady=5)

        self.table.pack(fill=tk.X, padx=90, pady=5)

        update_button.pack(fill=tk.X, padx=40, pady=5)
        back_button.pack(fill=tk.X, padx=40, pady=5)

    def refresh_data(self):
        """Pull new data from the database"""

        # Get the latest data
        result = self.controller.extract_message_data()

        # Error handling
        if result[0] != "success":
            self.controller.show_error(f"Database error! Error: {result[0]}")

        else:
            data = result[1]
            self.update_table(data)

    def update_table(self, data):
        """Update the display element"""

        # Clear the table
        self.table.delete(*self.table.get_children())

        # Column headings
        col_refs = ("#0", "message", "author", "date")
        col_heads = ("id", "message", "author", "date")

        # Loop through columns, setting each column
        # to the same width with the correct name
        for col in range(4):
            self.table.column(col_refs[col], width=155, stretch=tk.NO)
            self.table.heading(col_refs[col], text=col_heads[col])

        # For each entry in the data, add a new row to the table
        for i in range(len(data)):
            row = data[i]
            self.table.insert("", i, text=row[0], values=row[1:])

        # Push the changes to the visible UI
        self.update()

    def update_UI(self):
        """Make immediate updates when the frame is loaded in"""

        # Reset the Frame size
        self.controller.geometry('800x400')
        self.focus_force()


# Create and run an instance of the app
app = Application()
app.mainloop()
