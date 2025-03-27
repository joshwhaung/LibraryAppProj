
# Library Book Management System

A **Library Book Management System** built with Python and Tkinter to manage books, borrowers, and due dates efficiently. This application provides an intuitive graphical user interface (GUI) for managing library operations such as adding, borrowing, returning, and tracking books.

Made with passion by Josh, Aron & Rog (Binary Brothers)

---

## Features

### 1. **Book Management**
- Add new books to the library with details like title, author, and genre.
- Remove selected books from the library.
- View all books in a searchable table with the following details:
  - **Book#**: A unique identifier for each book.
  - **Title**, **Author**, **Genre**.
  - **Status**: Indicates whether the book is available, borrowed, or overdue.
  - **Borrower Name**, **Last Borrowed Date**, **Due Date**.

### 2. **Borrow and Return Books**
- Borrow books by entering the title and borrower's name.
- Automatically calculate and display the due date based on the configured due date days.
- Return books and update their status to "available."

### 3. **Dynamic Due Date Configuration**
- Change the default due date days dynamically from the **Settings** tab.
- Automatically update the due dates of all currently borrowed books when the due date days are changed.

### 4. **Statistics and Analytics**
- View detailed statistics in the **Statistics** tab:
  - **Most Popular Books**: Displays books with the highest borrow count.
  - **Overdue Books**: Lists books that are overdue along with the number of days past due.
  - **Most Borrowed Borrowers**: Shows borrowers who have borrowed the most books.

### 5. **Responsive and Scrollable UI**
- Fully responsive layout that adjusts to different screen sizes.
- Scrollable sections for managing large datasets.

### 6. **Search Functionality**
- Search books by title, author, or genre in real-time.

---

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Required Python libraries:
  - `tkinter` (comes pre-installed with Python).
  - `datetime` (comes pre-installed with Python).

### Steps
1. Clone or download the repository:
   ```bash
   git clone https://github.com/your-repo/library-management-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd library-management-system
   ```
3. Install any additional dependencies (if required):
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python Library.py
   ```

---

## Usage

### 1. **Adding a Book**
- Navigate to the **Management** tab.
- Enter the book's title, author, and genre in the "Add a New Book" section.
- Click the **Add Book** button to add the book to the library.

### 2. **Borrowing a Book**
- Navigate to the **Management** tab.
- Enter the book's title and the borrower's name in the "Borrow a Book" section.
- Click the **Borrow Book** button to borrow the book.

### 3. **Returning a Book**
- Navigate to the **Management** tab.
- Enter the book's title in the "Return a Book" section.
- Click the **Return Book** button to return the book.

### 4. **Changing Due Date Days**
- Navigate to the **Settings** tab.
- Enter the new due date days in the input field.
- Click the **Update Due Date Days** button to apply the changes.

### 5. **Viewing Statistics**
- Navigate to the **Statistics** tab.
- View the following tables:
  - **Most Popular Books**.
  - **Overdue Books**.
  - **Most Borrowed Borrowers**.
- Click the **Refresh All Tables** button to update the statistics.

---

## File Structure

```
Library.py                # Main application file
library_data.json         # JSON file to store library data
README.md                 # Documentation file

```

## Future Enhancements
- Add user authentication for library staff.
- Export library data to CSV or Excel format.
- Add email notifications for overdue books.
- Implement a dark mode for the UI.
