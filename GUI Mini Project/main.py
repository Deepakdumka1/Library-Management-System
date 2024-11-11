import os
import getpass
import sqlite3 as db

MAX_STRING_LENGTH = 50
MAX_TITLE_LENGTH = 100
MAX_TITLES = 100
MAX_MEMBERS = 100
FINE_PER_DAY = 4.0  # Fine per overdue day

# Define the Book and Member data structures
class Book:
    def __init__(self, book_id, book_name, author, no_of_titles, titles, status):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.no_of_titles = no_of_titles
        self.titles = titles
        self.status = status

class Member:
    def __init__(self, member_id, name, fines):
        self.member_id = member_id
        self.name = name
        self.fines = fines

# Global variables
books = []
members = []

# Function prototypes


# function for adding the books
def add_book():
    book_id = int(input("Enter The ID of The Book: "))
    book_name = input("Enter The Name of The Book: ")
    author = input("Enter The Name of Author: ")
    no_of_titles = int(input("Enter The Number of Titles Of The Book: "))

    if no_of_titles > MAX_TITLES:
        print("Number of titles exceeds the maximum allowed.")
        return

    titles = []
    for _ in range(no_of_titles):
        title = input("Enter a Title of The Book: ")
        titles.append(title)

    book = Book(book_id, book_name, author, no_of_titles, titles, 1)  # 1 for 'IN'
    books.append(book)

    with open("librecord.txt", "a") as librecord:
        librecord.write(f"{book.book_id}\t{book.book_name}\t{book.author}\t{book.status}\t{book.no_of_titles}\t")
        librecord.write("\t".join(book.titles) + "\n")

    print("A New Book has been Added Successfully...")


# function for displaying the books
def display_books():
    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    with open("librecord.txt", "r") as librecord:
        print("\nBookid\tName\tAuthor\tStatus\tNo.\tTitles")
        for line in librecord:
            print(line.strip())

    if not os.path.exists("member_record.txt"):
        print("Error opening member records file.")
        return

    with open("member_record.txt", "r") as member_record:
        print("\nMid\tName\tDept\tPh.no\tAvailablecards")
        for line in member_record:
            print(line.strip())


# function for searching the books by name
def search_book():
    book_found = False
    name_of_book = input("Enter The Name Of Book: ")

    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    with open("librecord.txt", "r") as librecord:
        lines = librecord.readlines()

    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) > 5 and parts[1] == name_of_book:
            book_id = int(parts[0])
            book_name = parts[1]
            author = parts[2]
            status = int(parts[3])
            no_of_titles = int(parts[4])
            titles = parts[5:]

            book_found = True
            book_status = "IN" if status == 1 else "OUT"

            print(f"\nThe Unique ID of The Book: {book_id}")
            print(f"The Name of Book is: {book_name}")
            print(f"The Author is: {author}")
            print(f"The Book Status: {book_status}")

            break

    if not book_found:
        print("\nBook Not Found!!")


# function for searching the books by author
def search_books_by_author():
    author_name = input("Enter the Author's Name: ").strip()
    found = False
    
    try:
        # Open the library record file for reading
        with open("librecord.txt", "r") as lib_file:
            for line in lib_file:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    book_author = parts[2]  # Assuming the author is the third column
                    if book_author.lower() == author_name.lower():
                        found = True
                        book_title = parts[1]  # Assuming the title is the second column
                        print(f"Book Title: {book_title}")
        
        if not found:
            print(f"No books found by author {author_name}.")
    
    except FileNotFoundError:
        print("Error: The library records file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


# function for displaying the books by author
def display_books_by_author():
    author_name = input("Enter The Name Of Author: ")

    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    found = False
    with open("librecord.txt", "r") as librecord:
        print("\nBooks:")
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                book_id = int(parts[0])
                book_name = parts[1]
                author = parts[2]
                status = int(parts[3])
                no_of_titles = int(parts[4])
                titles = parts[5:]

                if author_name == author:
                    found = True
                    print(f"\n\t{book_name}")

    if not found:
        print("There is no such Entry...!!")


# function for diaplaying the titles of the books
def list_titles_of_book():
    book_name = input("Enter The Book Name: ")
    
    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    found = False
    with open("librecord.txt", "r") as librecord:
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                book_id = int(parts[0])
                current_book_name = parts[1]
                author = parts[2]
                status = int(parts[3])
                no_of_titles = int(parts[4])
                titles = parts[5:]

                if book_name == current_book_name:
                    found = True
                    print(f"The Name of book is: {current_book_name}")
                    print("\nThe Titles:\n")
                    for i, title in enumerate(titles):
                        print(f"{i + 1}. {title}......")
                    break

    if not found:
        print("There is no such Entry...!!")


# function for displaying stock count
def display_stock_count():
    stock_count = 0
    
    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    with open("librecord.txt", "r") as librecord:
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                status = int(parts[3])

                if status == 1:  # Assuming '1' means the book is in stock
                    stock_count += 1

    print(f"\nCount of Books in Stock: {stock_count}")


# function for displaying the issue count
def display_issued_count():
    issued_count = 0
    
    if not os.path.exists("librecord.txt"):
        print("Error in opening the file...!!")
        return

    with open("librecord.txt", "r") as librecord:
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                status = int(parts[3])

                if status == 0:  # Assuming '0' means the book is issued
                    issued_count += 1

    print(f"\nCount of Issued Books: {issued_count}")


# function for returning the books


# Function to return a book
def return_book():
    # Step 1: Input the Book ID to return
    book_id = int(input("Enter the Book ID to return: "))
    found = False

    # Step 2: Check if the library record file exists
    if not os.path.exists("librecord.txt"):
        print("Error: Book records file 'librecord.txt' does not exist.")
        return

    # Step 3: Create a temporary file to update the book status to "IN" if it was issued
    temp_file = "temp_librecord.txt"
    with open("librecord.txt", "r") as librecord, open(temp_file, "w") as temp_file_obj:
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                current_book_id = int(parts[0])
                status = int(parts[3])  # Assuming '3' is the index for the book status

                if current_book_id == book_id:
                    # Check if the book is currently issued (OUT) and update it to IN
                    if status == 0:  # Assuming '0' means the book is issued
                        status = 1  # Update to IN
                        found = True
                        print(f"Book ID {book_id} found. Updating status to IN.")
                    else:
                        print(f"Book ID {book_id} is already in stock.")

                # Write the updated or original record to the temporary file
                temp_file_obj.write("\t".join([str(current_book_id)] + parts[1:4] + [str(status)] + parts[5:]) + "\n")

    # Replace the original file with the updated one
    os.replace(temp_file, "librecord.txt")

    if found:
        # Prompt for the Member ID who is returning the book
        member_id = int(input("Enter the Member ID who is returning the book: "))

        # Update the member's record in the member_record.txt file if needed
        if not os.path.exists("member_record.txt"):
            print("Member records file not found, creating a new one.")
            with open("member_record.txt", "w") as file:
                # Optionally, add headers or initial data structure
                file.write("MemberID Name Fines\n")

        # Update fines for the member if needed
        with open("member_record.txt", "r") as member_record:
            lines = member_record.readlines()

        with open("member_record.txt", "w") as member_record:
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 3:
                    current_member_id = int(parts[0])
                    fines = float(parts[2])

                    if current_member_id == member_id:
                        # Reset fines if applicable or apply late fee logic
                        fines = max(fines, 0)
                        print(f"Member ID {member_id} record updated with fines cleared.")
                        member_record.write(f"{current_member_id} {parts[1]} {fines:.2f}\n")
                    else:
                        member_record.write(line)
    else:
        print(f"Book ID {book_id} not found or already in stock.")


def take_input(prompt):
    """Take user input and strip newline characters."""
    return input(prompt).strip()


# function for generating user name
def generate_username(email):
    """Generate a username from the email."""
    return email.split('@')[0]

# function for taking psswd
def take_password():
    """Take password input securely without echoing characters."""
    return getpass.getpass("Enter password: ")


# function for adding members
def add_member():
    """Add a new member to the binary file."""
    file_name = "members.dat"

    # Collect member details
    member_id = int(input("Enter member ID: "))
    name = take_input("Enter member name: ")
    contact_no = take_input("Enter contact number: ")

    # Define member data structure
    member_data = {
        'member_id': member_id,
        'name': name,
        'contact_no': contact_no
    }

    # Append to the binary file
    with open(file_name, "ab") as file:
        # Write the member data as bytes
        file.write(member_id.to_bytes(4, byteorder='little'))
        file.write(len(name).to_bytes(1, byteorder='little'))
        file.write(name.encode('utf-8'))
        file.write(len(contact_no).to_bytes(1, byteorder='little'))
        file.write(contact_no.encode('utf-8'))

    print("Member added successfully.")
# function for removing the members
def remove_member():
    member_id = int(input("Enter the Member ID to remove: "))
    found = False

    # Open the member record file for reading
    try:
        with open("member_record.txt", "r") as member_file:
            # Create a temporary file to write the remaining records
            with open("temp_member_record.txt", "w") as temp_file:
                # Read the member records and write to the temporary file, skipping the member to be removed
                for line in member_file:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        current_id, name, fines = int(parts[0]), parts[1], float(parts[2])
                        if current_id != member_id:
                            # Write the record to the temporary file
                            temp_file.write(f"{current_id} {name} {fines:.2f}\n")
                        else:
                            found = True
                            print(f"Member ID {member_id} has been removed.")
                            
    except FileNotFoundError:
        print("Error opening the member records file.")
        return
    if not found:
        print(f"Member ID {member_id} not found.")
    
    # Replace the original file with the updated one
    os.remove("member_record.txt")
    os.rename("temp_member_record.txt", "member_record.txt")


# function for paying fines
def pay_fines():
    member_id = int(input("Enter the Member ID to pay fines: "))
    payment_amount = float(input("Enter the amount to pay: "))
    found = False

    # Open the member record file for reading and updating
    try:
        with open("member_record.txt", "r+") as member_file:
            lines = member_file.readlines()
            member_file.seek(0)
            member_file.truncate()
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 3:
                    current_id, name, fines = int(parts[0]), parts[1], float(parts[2])
                    if current_id == member_id:
                        found = True
                        print(f"Current fines for Member ID {member_id}: {fines:.2f}")
                        if payment_amount <= 0:
                            print("Invalid payment amount. It should be greater than zero.")
                            return
                        fines -= payment_amount
                        if fines < 0:
                            fines = 0
                        print("Fines updated successfully.")
                        member_file.write(f"{current_id} {name} {fines:.2f}\n")
                    else:
                        member_file.write(f"{current_id} {name} {fines:.2f}\n")
            
            if not found:
                print(f"Member ID {member_id} not found.")
                
    except FileNotFoundError:
        print("Error opening the member records file.")


# function for removing the books
def remove_book():
    book_id = int(input("Enter the Book ID to remove: "))
    found = False

    try:
        # Open the library record file for reading
        with open("librecord.txt", "r") as lib_file:
            lines = lib_file.readlines()

        # Create a temporary file for writing the remaining records
        with open("temp_librecord.txt", "w") as temp_file:
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    current_id = int(parts[0])
                    if current_id != book_id:
                        # Write the record to the temporary file
                        temp_file.write('\t'.join(parts) + '\n')
                    else:
                        found = True
                        print(f"Book ID {book_id} has been removed.")
                
        if not found:
            print(f"Book ID {book_id} not found.")
        
        # Replace the old file with the updated file
        os.remove("librecord.txt")
        os.rename("temp_librecord.txt", "librecord.txt")
    
    except FileNotFoundError:
        print("Error opening the library records file.")
    except Exception as e:
        print(f"An error occurred: {e}")


# function for issuing the books
def issue_book():
    # Step 1: Input the Book ID to issue
    book_id = int(input("Enter the Book ID to issue: "))
    found = False

    # Step 2: Check if the library record file exists
    if not os.path.exists("librecord.txt"):
        print("Error: Book records file 'librecord.txt' does not exist.")
        return

    # Step 3: Create a temporary file to update the book status to "OUT" if available
    temp_file = "temp_librecord.txt"
    with open("librecord.txt", "r") as librecord, open(temp_file, "w") as temp_file_obj:
        for line in librecord:
            parts = line.strip().split("\t")
            if len(parts) > 5:
                current_book_id = int(parts[0])
                status = int(parts[3])  # Assuming '3' is the index for the book status

                if current_book_id == book_id:
                    # Check if the book is available (IN) and update it to OUT
                    if status == 1:  # Assuming '1' means the book is in stock
                        status = 0  # Update to OUT
                        found = True
                        print(f"Book ID {book_id} found. Updating status to OUT.")
                    else:
                        print(f"Book ID {book_id} is already issued.")

                # Write the updated or original record to the temporary file
                temp_file_obj.write("\t".join([str(current_book_id)] + parts[1:4] + [str(status)] + parts[5:]) + "\n")

    # Replace the original file with the updated one
    os.replace(temp_file, "librecord.txt")

    if found:
        # Prompt for the Member ID to whom the book is issued
        member_id = int(input("Enter the Member ID who is issuing the book: "))
        print(f"Book ID {book_id} issued to Member ID {member_id}.")
    else:
        print(f"Book ID {book_id} not found or already issued.")
def update_book():
    book_id = int(input("Enter The ID of The Book to Update: "))
    found = False

    try:
        # Open the library record file for reading
        with open("librecord.txt", "r") as lib_file:
            lines = lib_file.readlines()
        
        # Create a temporary file for writing updated data
        with open("temp_librecord.txt", "w") as temp_file:
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    current_id = int(parts[0])
                    if current_id == book_id:
                        found = True
                        print("Book found. Enter new details:")

                        # Get new details from the user
                        title = input("Enter new title: ")
                        author = input("Enter new author: ")
                        status = int(input("Enter new status (1 for IN, 0 for OUT): "))
                        # Ensure the status is either 0 or 1
                        if status not in [0, 1]:
                            print("Invalid status. Status must be 0 or 1.")
                            return

                        # Assuming we have 5 fields; update the necessary fields
                        temp_file.write(f"{book_id}\t{title}\t{author}\t{status}\t{parts[4]}\n")
                    else:
                        temp_file.write(line)
        
        if not found:
            print(f"The Book with ID {book_id} was not found.")
        
        # Replace the old file with the updated file
        os.replace("temp_librecord.txt", "librecord.txt")

    except FileNotFoundError:
        print("Error: The library records file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#function to limit number or books issued
def limit_books_issued():
    issued_count = 0
    issue_limit = 5
    temp_file = "temp_librecord.txt"
    
    # Check if the file exists
    if not os.path.exists("librecord.txt"):
        print("Error: File 'librecord.txt' does not exist.")
        return

    # Count the number of issued books
    with open("librecord.txt", "r") as librecord:
        lines = librecord.readlines()

    for line in lines:
        parts = line.strip().split("\t")
        
        # Ensure that the line has enough parts
        if len(parts) > 5:
            try:
                status = int(parts[3])
                # Check if the book is issued (status == 0)
                if status == 0:
                    issued_count += 1
            except ValueError:
                print(f"Warning: Invalid status value found in line: {line.strip()}")
    
    # Check if the issue limit is reached
    if issued_count >= issue_limit:
        print(f"Cannot issue more books. The limit of {issue_limit} issued books has been reached.")
        return
    
    # Proceed to issue a new book
    print(f"You can issue more books. Currently, {issued_count} books are issued.")
    book_id_to_issue = input("Enter the ID of the book you want to issue: ").strip()

    # Update the file with the new book issuance
    with open("librecord.txt", "r") as librecord, open(temp_file, "w") as temp_file:
        for line in librecord:
            parts = line.strip().split("\t")
            
            # Ensure that the line has enough parts
            if len(parts) > 5:
                try:
                    book_id = parts[0]
                    status = int(parts[3])
                    
                    # Update the status of the book with the matching ID
                    if book_id == book_id_to_issue and status != 0:
                        status = 0  # Set status to 0 indicating the book is issued
                        print(f"Book ID {book_id} has been issued successfully.")
                    
                    # Write the updated or unchanged line to the temporary file
                    temp_file.write("\t".join([str(status) if i == 3 else part for i, part in enumerate(parts)]) + "\n")
                except ValueError:
                    print(f"Warning: Invalid status value found in line: {line.strip()}")
    
    # Replace the original file with the updated temporary file
    os.replace(temp_file, "librecord.txt")        
        
# function to display books by name     
def display_books_by_name():
    book_name_query = input("Enter the name of the book: ").strip()

    # Check if the file exists
    if not os.path.exists("librecord.txt"):
        print("Error: File 'librecord.txt' does not exist.")
        return

    found = False

    # Open the file and read line by line
    with open("librecord.txt", "r") as librecord:
        print(f"\nBooks matching '{book_name_query}':")
        for line in librecord:
            parts = line.strip().split("\t")
            
            # Ensure that the line has enough parts
            if len(parts) > 5:
                book_id = parts[0]
                book_name = parts[1]
                author = parts[2]
                status = parts[3]
                no_of_titles = parts[4]
                titles = parts[5:]

                # Check if the book name matches
                if book_name_query.lower() in book_name.lower():
                    found = True
                    print(f"\nBook ID: {book_id}")
                    print(f"Book Name: {book_name}")
                    print(f"Author: {author}")
                    print(f"Status: {status}")
                    print(f"Number of Titles: {no_of_titles}")
                    print(f"Titles: {', '.join(titles)}")

    # Inform the user if no books by the name were found
    if not found:
        print("No books found with this name.")
        
#function to reserve books
def reserve_book():
    book_id = int(input("Enter Book ID to Reserve: "))
    member_id = int(input("Enter Your Member ID: "))

    if not os.path.exists("librecord.txt"):
        print("Library records file does not exist.")
        return
    
    found = False
    with open("librecord.txt", "r") as librecord:
        lines = librecord.readlines()
    
    with open("reservations.txt", "a") as reservation_file:
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            current_book_id = int(parts[0])
            status = int(parts[3])
            
            if current_book_id == book_id and status == 1:  # Assuming 1 for 'IN' status
                reservation_file.write(f"{book_id} {member_id}\n")
                print("Book reserved successfully.")
                found = True
                break
    
    if not found:
        print("Book is not available for reservation.")
  
# function to update member details
def update_member():
    member_id = int(input("Enter The ID of The Member to Update: "))
    found = False

    try:
        # Open the members record file for reading
        with open("members.txt", "r") as members_file:
            lines = members_file.readlines()
        
        # Create a temporary file for writing updated data
        with open("temp_members.txt", "w") as temp_file:
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    current_id = int(parts[0])
                    if current_id == member_id:
                        found = True
                        print("Member found. Enter new details:")

                        # Get new details from the user
                        name = input("Enter new name: ")
                        email = input("Enter new email: ")
                        phone = input("Enter new phone number: ")

                        # Update the record with new details
                        temp_file.write(f"{member_id}\t{name}\t{email}\t{phone}\n")
                    else:
                        temp_file.write(line)
        
        if not found:
            print(f"The Member with ID {member_id} was not found.")
        
        # Replace the old file with the updated file
        os.replace("temp_members.txt", "members.txt")

    except FileNotFoundError:
        print("Error: The members records file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
# Main function integration

def run():
    while True:
        print("\n\t\t\t*********************************************************************************************")
        print("\n\t\t\t\t\t\t\tWELCOME TO THE LIBRARY\n")
        print("\t\t\t*********************************************************************************************")
        choice1 = int(input("\n\n\t\t\t\tPRESS 1 TO LOGIN AS A LIBRARIAN\n"
                            "\t\t\t\tPRESS 2 TO LOGIN AS A USER\n"
                            "\n\t\t\t\t Enter your choice: "))

        if choice1 == 1:
            while True:
                print("\n\n\t--MENU--\n\n"
                      "1. Add A New Book\n"
                      "2. Search a Book\n"
                      "3. Display Complete Information\n"
                      "4. Display All Books of An Author\n"
                      "5. List Titles of a Book\n"
                      "6. List Count of Issued Books\n"
                      "7. To Issue a Book\n"
                      "8. To Return a Book\n"
                      "9. Add A New Member\n"
                      "10. To Remove a Book\n"
                      "11. To Remove a Member\n"
                      "12. Update Book Details\n"
                      "13. Update Member Details\n"  
                      "14. Exit the Program\n\n")

                choice2 = int(input("\t Enter your choice <1-14>: "))
                if choice2 == 1:
                    add_book() 
                elif choice2 == 2:
                    search_book() 
                elif choice2 == 3:
                    display_books() 
                elif choice2 == 4:
                    display_books_by_author()  
                elif choice2 == 5:
                    list_titles_of_book()  
                elif choice2 == 6:
                    display_issued_count()  
                elif choice2 == 7:
                    issue_book()  
                elif choice2 == 8:
                    return_book()
                elif choice2 == 9:
                    add_member()  
                elif choice2 == 10:
                    remove_book()  
                elif choice2 == 11:
                    remove_member()  
                elif choice2 == 12:
                    update_book()  
                elif choice2 == 13:
                    update_member()  
                elif choice2 == 14:
                    print("Exiting the program...")
                    break
                else:
                    print("Invalid Input...!! Please enter a valid choice!!")
        elif choice1 == 2:
            while True:
                print("\n\n\t--MENU--\n\n"
                      "1. Display Complete Information\n"
                      "2. Display All Books of An Author\n"
                      "3. Display Books By Name\n"
                      "4. List Titles of a Book\n"
                      "5. Fine\n"
                      "6. Exit the Program\n\n")

                choice2 = int(input("\t Enter your choice <1-5>: "))

                if choice2 == 1:
                    display_books()  
                elif choice2 == 2:
                    display_books_by_author()  
                elif choice2 == 3:
                     display_books_by_name()
                elif choice2 == 4:
                    list_titles_of_book()  
                elif choice2 == 5:
                    pay_fines()  
                elif choice2 == 6:
                    print("Exiting the program...")
                    break
                else:
                    print("Invalid Input...!! Please enter a valid choice!!")

        else:
            print("\n\t\t\t\t_Enter valid choice_")
run()

