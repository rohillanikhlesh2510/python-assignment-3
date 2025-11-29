# cli/main.py
"""
Command-line interface for the Library Inventory Manager.
Handles user interaction and input validation.
"""

import logging
from pathlib import Path

from library_manager.inventory import LibraryInventory

# Configure root logger
LOG_PATH = Path(_file_).resolve().parents[1] / "library.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(_name_)

DATA_FILE = Path(_file_).resolve().parents[1] / "data" / "catalog.json"

def prompt(prompt_text: str) -> str:
    """Simple wrapper for input to allow future changes (e.g., GUI)."""
    return input(prompt_text).strip()

def print_menu():
    print("\n--- Library Inventory Manager ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("0. Exit")

def main():
    # Initialize inventory
    inventory = LibraryInventory(storage_path=DATA_FILE)
    print("Welcome to Library Inventory Manager.")
    while True:
        try:
            print_menu()
            choice = prompt("Choose an option (0-6): ")
            if choice == "1":
                title = prompt("Enter book title: ")
                author = prompt("Enter author name: ")
                isbn = prompt("Enter ISBN: ")
                try:
                    book = inventory.add_book(title=title, author=author, isbn=isbn)
                    print(f"Book added: {book}")
                except ValueError as ve:
                    print(f"Error: {ve}")

            elif choice == "2":
                isbn = prompt("Enter ISBN to issue: ")
                try:
                    success = inventory.issue_book(isbn)
                    if success:
                        print("Book issued successfully.")
                    else:
                        print("Book was already issued.")
                except LookupError as le:
                    print(f"Error: {le}")

            elif choice == "3":
                isbn = prompt("Enter ISBN to return: ")
                try:
                    success = inventory.return_book(isbn)
                    if success:
                        print("Book returned successfully.")
                    else:
                        print("Book was not issued.")
                except LookupError as le:
                    print(f"Error: {le}")

            elif choice == "4":
                books = inventory.display_all()
                if not books:
                    print("No books in inventory.")
                else:
                    print("\nBooks in inventory:")
                    for bstr in books:
                        print(" -", bstr)

            elif choice == "5":
                q = prompt("Enter title search query: ")
                results = inventory.search_by_title(q)
                if results:
                    print(f"Found {len(results)} result(s):")
                    for b in results:
                        print(" -", b)
                else:
                    print("No books matched the title query.")

            elif choice == "6":
                isbn = prompt("Enter ISBN to search: ")
                b = inventory.search_by_isbn(isbn)
                if b:
                    print("Found:", b)
                else:
                    print("No book found with that ISBN.")

            elif choice == "0":
                print("Goodbye — saving data and exiting.")
                inventory.save_to_file()
                break

            else:
                print("Invalid choice. Please choose a number between 0 and 6.")

        except KeyboardInterrupt:
            print("\nInterrupted by user — saving and exiting.")
            inventory.save_to_file()
            break
        except Exception as e:
            # Catch-all to ensure CLI does not crash unexpectedly
            logger.exception(f"Unexpected error in CLI: {e}")
            print(f"An unexpected error occurred: {e}")

if _name_ == "_main_":
    main()
