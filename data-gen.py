import sqlite3
import os
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_phone_number():
    # Ensure the first digit is not 0
    first_digit = random.randint(1, 9)

    # Generate the remaining 9 digits
    remaining_digits = [str(random.randint(0, 9)) for _ in range(9)]

    # Combine all digits into a single string
    all_digits = str(first_digit) + "".join(remaining_digits)

    # Format the phone number with dashes
    formatted_number = f"{all_digits[0:3]}-{all_digits[3:6]}-{all_digits[6:10]}"
    
    return formatted_number



def generate_test_data(num_contacts):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = generate_phone_number()
        db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.
