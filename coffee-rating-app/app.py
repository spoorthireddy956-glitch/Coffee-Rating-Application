from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            votes INTEGER
        )
    ''')
    
    # Insert sample data
    coffees = [
        ('Ethiopian Yirgacheffe', 0),
        ('Sumatra Mandheling', 0),
        ('Cold Brew Nitro', 0),
        ('Vanilla Latte', 0),
        ('Mexican Chiapas', 0)
    ]
    
    c.executemany("INSERT INTO coffee (name, votes) VALUES (?, ?)", coffees)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM coffee")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', coffees=data)

@app.route('/vote', methods=['POST'])
def vote():
    coffee_id = request.json['id']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE coffee SET votes = votes + 1 WHERE id=?", (coffee_id,))
    conn.commit()
    
    c.execute("SELECT votes FROM coffee WHERE id=?", (coffee_id,))
    votes = c.fetchone()[0]
    conn.close()

    return jsonify({'votes': votes})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)