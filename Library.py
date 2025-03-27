import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime, timedelta

# File to store library data
FILE_NAME = "library_data.json"

# Initialize library data
def load_library():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_library():
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

# Global variable for due date days
DUE_DATE_DAYS = 7  # Default value

def update_due_date_days():
    """Update the number of days for the due date."""
    global DUE_DATE_DAYS
    try:
        new_days = int(entry_due_date_days.get())
        if new_days > 0:
            DUE_DATE_DAYS = new_days
            messagebox.showinfo("Success", f"Due date days updated to {DUE_DATE_DAYS} days.")
        else:
            messagebox.showerror("Error", "Please enter a positive number.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

# Functions for library operations
def view_books():
    # Clear the existing records in the Treeview
    for row in books_tree.get_children():
        books_tree.delete(row)
    
    query = search_entry.get().lower()
    for i, (title, details) in enumerate(library.items(), start=1):
        if query in title.lower() or query in details['author'].lower() or query in details['genre'].lower():
            status = details['status']
            borrower = details['borrower']
            last_borrowed_date = details.get('borrowed_date', "")  # Get Last Borrowed Date or default to empty
            due_date = details['due_date'] if details['due_date'] else ""
            
            # Determine the status color
            if status == "available":
                status_color = "green"
            elif status == "borrowed":
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
                if due_date_obj and due_date_obj < datetime.now():
                    status = "overdue"
                    status_color = "red"
                else:
                    status_color = "black"
            else:
                status_color = "black"
            
            # Insert the book details into the Treeview
            books_tree.insert(
                "",
                tk.END,
                values=(f"{i:04d}", title, details['author'], details['genre'], status, borrower, last_borrowed_date, due_date),
                tags=(status_color,)  # Apply color only to the Status column
            )
    
    # Configure tags for color (only for the Status column)
    books_tree.tag_configure("green", foreground="green")  # Available
    books_tree.tag_configure("black", foreground="black")  # Borrowed
    books_tree.tag_configure("red", foreground="red")  # Overdue

def add_book():
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()

    if title and author and genre:
        if title in library:
            messagebox.showerror("Error", "Book already exists in the library.")
        else:
            library[title] = {"author": author, "genre": genre, "status": "available", "borrower": None, "due_date": None}
            save_library()
            messagebox.showinfo("Success", "Book added successfully!")
            view_books()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def remove_selected_books():
    selected_items = books_tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "No books selected.")
        return
    
    for item in selected_items:
        title = books_tree.item(item, "values")[1]  # Get the title from the selected row
        if title in library:
            del library[title]
    
    save_library()
    messagebox.showinfo("Success", "Selected books have been removed.")
    view_books()

    
def borrow_book():
    title = entry_borrow_title.get()
    borrower = entry_borrower_name.get()

    if title in library:
        if library[title]['status'] == "available":
            library[title]['status'] = "borrowed"
            library[title]['borrower'] = borrower
            library[title]['borrowed_date'] = datetime.now().strftime("%Y-%m-%d")  # Add Last Borrowed Date
            library[title]['due_date'] = (datetime.now() + timedelta(days=DUE_DATE_DAYS)).strftime("%Y-%m-%d")
            library[title]['borrow_count'] += 1  # Increment the borrow count
            save_library()
            messagebox.showinfo("Success", f"You have borrowed '{title}'.")
            view_books()
        else:
            messagebox.showerror("Error", f"'{title}' is already borrowed by {library[title]['borrower']}.")
    else:
        messagebox.showerror("Error", "Book not found in the library.")

def return_book():
    title = entry_return_title.get()

    if title in library:
        if library[title]['status'] == "borrowed":
            library[title]['status'] = "available"
            library[title]['borrower'] = None
            library[title]['due_date'] = None
            save_library()
            messagebox.showinfo("Success", f"'{title}' has been returned.")
            view_books()
        else:
            messagebox.showerror("Error", f"'{title}' is not currently borrowed.")
    else:
        messagebox.showerror("Error", "Book not found in the library.")

# Add a new field to track the number of times a book has been borrowed
for book in library.values():
    if 'borrow_count' not in book:
        book['borrow_count'] = 0

def view_popular_books():
    # Clear the existing records in the Treeview
    for row in popular_tree.get_children():
        popular_tree.delete(row)
    
    # Sort books by borrow count in descending order
    sorted_books = sorted(library.items(), key=lambda item: item[1]['borrow_count'], reverse=True)
    
    for i, (title, details) in enumerate(sorted_books, start=1):
        if details['borrow_count'] > 0:
            popular_tree.insert("", tk.END, values=(i, title, details['author'], details['borrow_count']))


def overdue_books():
    # Clear the existing records in the Treeview
    for row in overdue_tree.get_children():
        overdue_tree.delete(row)
    for i, (title, details) in enumerate(library.items(), start=1):
        if details['status'] == "borrowed":
            due_date = datetime.strptime(details['due_date'], "%Y-%m-%d")
            if due_date < datetime.now():
                days_past_due = (datetime.now() - due_date).days
                overdue_tree.insert("", tk.END, values=(i, title, details['borrower'], details['due_date'], days_past_due))

# Function to sort Treeview columns
def sort_treeview(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # Reorder the items in the Treeview
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # Reverse the sorting order
    tv.heading(col, command=lambda _col=col: sort_treeview(tv, _col, not reverse))

# GUI setup
root = tk.Tk()
root.title("Library Book Management System")
root.geometry("1200x900")

# Create a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Management Tab
management_tab = ttk.Frame(notebook)
notebook.add(management_tab, text="Management")

# Settings Tab
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="Settings")

# Add a new "Statistics" tab
statistics_tab = ttk.Frame(notebook)
notebook.add(statistics_tab, text="Statistics")

# Management Tab Content
main_frame = ttk.Frame(management_tab)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# View Books Section
tk.Label(scrollable_frame, text="Search Books", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Label(scrollable_frame, text="Search by Title, Author, or Genre:", bg="#f0f0f0").pack()
search_entry = ttk.Entry(scrollable_frame, width=50)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda event: view_books())  # Call view_books on key release

tk.Label(scrollable_frame, text="Library Books", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# Update the columns for the Library Books Table
columns = ("Book#", "Title", "Author", "Genre", "Status", "Borrower Name", "Last Borrowed Date", "Due Date")
books_tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=20, selectmode="extended")
for col in columns:
    books_tree.heading(col, text=col, command=lambda _col=col: sort_treeview(books_tree, _col, False))

# Set column widths
books_tree.column("Book#", width=50, anchor="center")
books_tree.column("Title", width=200)
books_tree.column("Author", width=200)
books_tree.column("Genre", width=150)
books_tree.column("Status", width=150)
books_tree.column("Borrower Name", width=200)
books_tree.column("Last Borrowed Date", width=150)
books_tree.column("Due Date", width=150)

# Configure tags for color (only for the Status column)
books_tree.tag_configure("green", foreground="green")
books_tree.tag_configure("black", foreground="black")
books_tree.tag_configure("red", foreground="red")

books_tree.pack(fill=tk.BOTH, expand=True, pady=10)

# Add buttons for removing selected books
button_frame = ttk.Frame(scrollable_frame)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Remove Selected Books", command=remove_selected_books).pack(side=tk.LEFT, padx=5)

view_books()

# Side-by-side layout for Book Management Section
tk.Label(scrollable_frame, text="Book Management", font=("Helvetica", 14, "bold")).pack(pady=10)
book_management_frame = ttk.Frame(scrollable_frame)
book_management_frame.pack(pady=10, fill=tk.X)

# Add Book Section
add_frame = ttk.LabelFrame(book_management_frame, text="Add a New Book", padding=10)
add_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
tk.Label(add_frame, text="Add a New Book", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
tk.Label(add_frame, text="Title:", bg="#f0f0f0").pack()
entry_title = ttk.Entry(add_frame, width=30)
entry_title.pack(pady=5)
tk.Label(add_frame, text="Author:", bg="#f0f0f0").pack()
entry_author = ttk.Entry(add_frame, width=30)
entry_author.pack(pady=5)
tk.Label(add_frame, text="Genre:", bg="#f0f0f0").pack()
entry_genre = ttk.Entry(add_frame, width=30)
entry_genre.pack(pady=5)
ttk.Button(add_frame, text="Add Book", command=add_book).pack(pady=10)

# Borrow Book Section
borrow_frame = ttk.LabelFrame(book_management_frame, text="Borrow a Book", padding=10)
borrow_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
tk.Label(borrow_frame, text="Borrow a Book", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
tk.Label(borrow_frame, text="Title:", bg="#f0f0f0").pack()
entry_borrow_title = ttk.Entry(borrow_frame, width=30)
entry_borrow_title.pack(pady=5)
tk.Label(borrow_frame, text="Your Name:", bg="#f0f0f0").pack()
entry_borrower_name = ttk.Entry(borrow_frame, width=30)
entry_borrower_name.pack(pady=5)
ttk.Button(borrow_frame, text="Borrow Book", command=borrow_book).pack(pady=10)

# Return Book Section
return_frame = ttk.LabelFrame(book_management_frame, text="Return a Book", padding=10)
return_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
tk.Label(return_frame, text="Return a Book", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
tk.Label(return_frame, text="Title:", bg="#f0f0f0").pack()
entry_return_title = ttk.Entry(return_frame, width=30)
entry_return_title.pack(pady=5)
ttk.Button(return_frame, text="Return Book", command=return_book).pack(pady=10)

# Settings Tab Content
tk.Label(settings_tab, text="Settings", font=("Arial", 18, "bold")).pack(pady=10)

# Change Due Date Days Section
tk.Label(settings_tab, text="Change Due Date Days:", font=("Arial", 14)).pack(pady=5)
entry_due_date_days = ttk.Entry(settings_tab, width=10)
entry_due_date_days.pack(pady=5)
entry_due_date_days.insert(0, str(DUE_DATE_DAYS))  # Set default value
ttk.Button(settings_tab, text="Update Due Date Days", command=update_due_date_days).pack(pady=10)

# Make the Statistics tab scrollable
statistics_frame = ttk.Frame(statistics_tab)
statistics_frame.pack(fill=tk.BOTH, expand=True)

statistics_canvas = tk.Canvas(statistics_frame)
statistics_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

statistics_scrollbar = ttk.Scrollbar(statistics_frame, orient=tk.VERTICAL, command=statistics_canvas.yview)
statistics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

statistics_scrollable_frame = ttk.Frame(statistics_canvas)
statistics_scrollable_frame.bind(
    "<Configure>",
    lambda e: statistics_canvas.configure(scrollregion=statistics_canvas.bbox("all"))
)

statistics_canvas.create_window((0, 0), window=statistics_scrollable_frame, anchor="nw")
statistics_canvas.configure(yscrollcommand=statistics_scrollbar.set)

# Statistics Tab Content
tk.Label(statistics_scrollable_frame, text="Statistics", font=("Arial", 18, "bold")).pack(pady=10)

# Most Popular Books Section
tk.Label(statistics_scrollable_frame, text="Most Popular Books", font=("Helvetica", 14, "bold")).pack(pady=10)
popular_columns = ("Book#", "Title", "Author", "AmountOfTimesBorrowed")
popular_tree = ttk.Treeview(statistics_scrollable_frame, columns=popular_columns, show="headings", height=10)
for col in popular_columns:
    popular_tree.heading(col, text=col)
popular_tree.column("Book#", width=50, anchor="center")
popular_tree.column("Title", width=200)
popular_tree.column("Author", width=200)
popular_tree.column("AmountOfTimesBorrowed", width=150)
popular_tree.pack(pady=5)

# Overdue Books Section
tk.Label(statistics_scrollable_frame, text="Overdue Books", font=("Helvetica", 14, "bold")).pack(pady=10)
overdue_columns = ("Book#", "Title", "Borrower Name", "Due Date", "Days Past Due")
overdue_tree = ttk.Treeview(statistics_scrollable_frame, columns=overdue_columns, show="headings", height=10)
for col in overdue_columns:
    overdue_tree.heading(col, text=col)
overdue_tree.column("Book#", width=50, anchor="center")
overdue_tree.column("Title", width=200)
overdue_tree.column("Borrower Name", width=200)
overdue_tree.column("Due Date", width=150)
overdue_tree.column("Days Past Due", width=150)
overdue_tree.pack(pady=5)

# Most Borrowed Borrower Section
tk.Label(statistics_scrollable_frame, text="Most Borrowed Borrowers", font=("Helvetica", 14, "bold")).pack(pady=10)
borrower_columns = ("Book#", "Borrower Name", "Books Borrowed")
borrower_tree = ttk.Treeview(statistics_scrollable_frame, columns=borrower_columns, show="headings", height=10)
for col in borrower_columns:
    borrower_tree.heading(col, text=col)
borrower_tree.column("Book#", width=50, anchor="center")
borrower_tree.column("Borrower Name", width=200)
borrower_tree.column("Books Borrowed", width=150)
borrower_tree.pack(pady=5)

# Function to populate the Most Popular Books table
def view_popular_books():
    for row in popular_tree.get_children():
        popular_tree.delete(row)
    sorted_books = sorted(library.items(), key=lambda item: item[1]['borrow_count'], reverse=True)
    for i, (title, details) in enumerate(sorted_books, start=1):
        if details['borrow_count'] > 0:
            popular_tree.insert("", tk.END, values=(i, title, details['author'], details['borrow_count']))

# Function to populate the Overdue Books table
def overdue_books():
    for row in overdue_tree.get_children():
        overdue_tree.delete(row)
    overdue_list = []
    for title, details in library.items():
        if details['status'] == "borrowed" and details['due_date']:
            due_date = datetime.strptime(details['due_date'], "%Y-%m-%d")
            if due_date < datetime.now():
                days_past_due = (datetime.now() - due_date).days
                overdue_list.append((title, details['borrower'], details['due_date'], days_past_due))
    overdue_list.sort(key=lambda x: x[3], reverse=True)  # Sort by days past due
    for i, (title, borrower, due_date, days_past_due) in enumerate(overdue_list, start=1):
        overdue_tree.insert("", tk.END, values=(i, title, borrower, due_date, days_past_due))

# Function to populate the Most Borrowed Borrowers table
def view_most_borrowed_borrowers():
    for row in borrower_tree.get_children():
        borrower_tree.delete(row)
    borrower_counts = {}
    for details in library.values():
        if details['borrower']:
            borrower_counts[details['borrower']] = borrower_counts.get(details['borrower'], 0) + 1
    sorted_borrowers = sorted(borrower_counts.items(), key=lambda item: item[1], reverse=True)
    for i, (borrower, count) in enumerate(sorted_borrowers, start=1):
        borrower_tree.insert("", tk.END, values=(i, borrower, count))

# Function to refresh all tables
def refresh_all_tables():
    view_popular_books()
    overdue_books()
    view_most_borrowed_borrowers()

# Add a single refresh button at the bottom
ttk.Button(statistics_scrollable_frame, text="Refresh All Tables", command=refresh_all_tables).pack(pady=10)

# Run the application
root.mainloop()