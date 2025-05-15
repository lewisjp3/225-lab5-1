import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def read_and_output_file(filepath):
    db = connect_db()
    with open(filepath, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            parts = cleaned_line.split(',')
            product = parts[0].strip()
            product = "Test " + product
            sku = parts[1].strip()
            db.execute('INSERT INTO products (product, sku) VALUES (?, ?)', (product, sku))
    db.commit()
    print(f'Test products added to the database.')
    db.close()

if __name__ == '__main__':
    filepath = 'products.csv'
    read_and_output_file(filepath)
