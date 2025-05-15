import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_sec_contacts():
    """Clear the contacts creatd by security checks."""
    db = connect_db()
    # All of the contacts created by the security check contain no spa
    db.execute("DELETE FROM contacts WHERE name NOT LIKE '% %'")
    db.commit()
    print('Security test contacts have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_sec_contacts()
