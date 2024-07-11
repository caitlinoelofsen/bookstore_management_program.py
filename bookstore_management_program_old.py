import sqlite3
import os
import sys

class Ebookstore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = self.connect_db()
        self.create_table()

    def connect_db(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        return sqlite3.connect(self.db_path)
    
    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book(
                   id INTEGER PRIMARY KEY,
                   title TEXT,
                   author TEXT,
                   qty INTEGER)
        ''')
        self.db.commit()

    def initialise_books(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT (*) FROM book')
        count = cursor.fetchone()[0]

        if count == 0:
            books = [            
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K Rowling', 40),
            (3003, 'The Lion the Witch and the Wardrobe', 'C.S Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
            ]

            cursor.executemany('''INSERT INTO book(id, title, author, qty)
                               VALUES (?,?,?,?)''', books)
            self.db.commit()

    @staticmethod
    def get_valid_int_input (prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("invalid input. Please enter a valid number.")
    
    def enter_book(self):
        cursor = self.db.cursor()
        id = self.get_valid_int_input('Enter new book id: ')
        title = input('Enter book title: ')
        author = input ('Enter author: ')
        qty = self.get_valid_int_input('Enter the quantity of stock: ')

        cursor.execute('''INSERT INTO book(id, title, author, qty)
                       VALUES(?,?,?,?)''', (id, title, author, qty))
        self.db.commit()

    def update_book(self):
        cursor = self.db.cursor()
        book_id = self.get_valid_int_input('Enter the ID of book to update: ')

        cursor.execute('SELECT * FROM book WHERE id = ?', (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book not found.")
            return
        
        new_id = book[0]
        new_title = book[1]
        new_author = book[2]
        new_qty = book[3]

        if input('Do you want to update the ID number? (Yes/No): ').strip().lower() == 'yes':
            new_id = self.get_valid_int_input('Update book ID number: ')

        if input('Do you want to update the book title? (Yes/No): ').strip().lower() == 'yes':
            new_title = input('Update book title: ')

        if input('Do you want to update the author? (Yes/No): ').strip().lower() == 'yes':
            new_author = input('Update author: ')

        if input('Do you want to update the quantity of stock: (Yes/No): ').strip().lower() == 'yes':
            new_qty = self.get_valid_int_input('Update quantity of stock: ')
               
        cursor.execute('''UPDATE book SET id = ?, title = ?, author = ? WHERE 
                       id = ?''',(new_id, new_title, new_author, new_qty))
        self.db.commit()
        print("Book updated successfully.")

    def delete_book(self):
        cursor = self.db.cursor()
        id = self.get_valid_int_input('Enter the ID number of the book: ')
        cursor.execute('''DELETE FROM book where id = ?''',(id,))
        self.db.commit()

    def search_books(self):
        cursor = self.db.cursor()
        title = input('Enter the book title: ')
        cursor.execute('''SELECT * FROM book WHERE title LIKE ?''',('%' + title + '%',))
        results  = cursor.fetchall()
        for row in results:
            print(row)

    def exit_program(self):
        print("Exiting the program...")
        self.db.close()
        sys.exit(0)

    def main_menu(self):
        while True:
            option = input('''Enter a menu option: 
              1. Enter book
              2. Update book
              3. Delete book
              4. Search books
              0. Exit
              ''')
            
            if option == '1':
                self.enter_book()
            elif option == '2':
                self.update_book()
            elif option == '3':
                self.delete_book()
            elif option == '4':
                self.search_books()
            elif option == '0':
                self.exit_program()
            else:
                print('Invalid input, please try again.')

if __name__ == "__main__":
    ebookstore = Ebookstore('data/ebookstore')
    ebookstore.initialise_books()
    ebookstore.main_menu()
