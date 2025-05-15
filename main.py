from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                sku TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM products WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Item deleted successfully.'
        else:
            name = request.form.get('product')
            phone = request.form.get('sku')
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO products (product, sku) VALUES (?, ?)', (product, sku))
                db.commit()
                message = 'Item added successfully.'
            else:
                message = 'Missing product name or SKU.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM products').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Products</title>
        </head>
        <body>
            <center><h2>Add Products</h2></center>
            <form method="POST" action="/">
                <label for="product">Product Name:</label><br>
                <input type="text" id="product" name="product" required><br>
                <label for="sku">SKU:</label><br>
                <input type="text" id="sku" name="sku" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if products %}
                <table border="1">
                    <tr>
                        <th>Product Name</th>
                        <th>SKU</th>
                        <th>Delete</th>
                    </tr>
                    {% for product in products %}
                        <tr>
                            <td>{{ product['product'] }}</td>
                            <td>{{ product['sku'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No items found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
